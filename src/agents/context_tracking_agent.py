"""Agent for tracking context between queries."""

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from typing import Dict, Any
import json


class ContextTrackingAgent:
    """Agent that determines if current query relates to previous analyses."""

    def __init__(self, model_name: str = "gpt-4-turbo-preview"):
        """Initialize the context tracking agent.

        Args:
            model_name: Name of the OpenAI model to use
        """
        self.llm = ChatOpenAI(model=model_name, temperature=0)

        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert at understanding conversational context in data analysis.

Your job is to determine if the current user query relates to or depends on previous analyses.

Previous Queries:
{previous_queries}

Current Analysis Intent:
{analysis_intent}

Determine:
1. Does this query reference previous results? (e.g., "show me more details", "break that down by", "what about")
2. Does this query build upon previous analysis?
3. What specific context from previous queries is relevant?

Respond in JSON format:
{{
    "requires_context": true/false,
    "context_description": "Description of how this relates to previous queries",
    "referenced_queries": ["indices of relevant previous queries"],
    "is_independent": true/false
}}"""),
            ("user", "{user_query}")
        ])

        self.chain = self.prompt | self.llm | StrOutputParser()

    def analyze(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Determine if current query needs context from previous queries.

        Args:
            state: Current agent state

        Returns:
            Updated state with context tracking information
        """
        user_query = state["user_query"]
        analysis_intent = state.get("analysis_intent", "")
        previous_queries = state.get("previous_queries", [])

        # Build previous queries summary
        prev_queries_text = ""
        if previous_queries:
            for i, query in enumerate(previous_queries):
                prev_queries_text += f"{i}: {query.get('description', 'N/A')}\n"
                prev_queries_text += f"   SQL: {query.get('sql_query', 'N/A')}\n\n"
        else:
            prev_queries_text = "No previous queries"

        # Analyze context requirements
        result = self.chain.invoke({
            "user_query": user_query,
            "analysis_intent": analysis_intent,
            "previous_queries": prev_queries_text
        })

        # Parse JSON response
        try:
            context_data = json.loads(result)
            requires_context = context_data.get("requires_context", False)
            context_description = context_data.get("context_description", "")
        except json.JSONDecodeError:
            # Fallback if JSON parsing fails
            requires_context = False
            context_description = result

        return {
            **state,
            "requires_context": requires_context,
            "context_description": context_description,
            "next_step": "sql_generation"
        }
