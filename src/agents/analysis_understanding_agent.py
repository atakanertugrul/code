"""Agent for understanding user's analysis intent."""

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from typing import Dict, Any
import json


class AnalysisUnderstandingAgent:
    """Agent that understands what analysis the user wants to perform."""

    def __init__(self, model_name: str = "gpt-4-turbo-preview"):
        """Initialize the analysis understanding agent.

        Args:
            model_name: Name of the OpenAI model to use
        """
        self.llm = ChatOpenAI(model=model_name, temperature=0)

        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert sales analyst. Your job is to understand what analysis the user wants to perform on sales data.

Given a user query, you need to:
1. Identify the specific analysis intent
2. Determine what metrics or insights they're looking for
3. Identify any specific filters, groupings, or aggregations needed

Database Schema:
{schema_info}

Previous context (if any):
{context}

Respond in JSON format with:
{{
    "analysis_intent": "Clear description of what analysis needs to be performed",
    "metrics_needed": ["list", "of", "metrics"],
    "filters": ["any", "filtering", "conditions"],
    "grouping": ["fields", "to", "group", "by"],
    "time_range": "any time-based filtering",
    "additional_notes": "any other relevant information"
}}"""),
            ("user", "{user_query}")
        ])

        self.chain = self.prompt | self.llm | StrOutputParser()

    def analyze(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze the user query to understand intent.

        Args:
            state: Current agent state

        Returns:
            Updated state with analysis intent
        """
        user_query = state["user_query"]
        schema_info = state.get("schema_info", "")

        # Build context from previous queries
        context = ""
        if state.get("previous_queries"):
            context = "Previous analyses:\n"
            for i, query in enumerate(state["previous_queries"][-3:], 1):
                context += f"{i}. {query.get('description', 'N/A')}\n"

        # Get analysis understanding
        result = self.chain.invoke({
            "user_query": user_query,
            "schema_info": schema_info,
            "context": context
        })

        # Parse JSON response
        try:
            analysis_data = json.loads(result)
            analysis_intent = analysis_data.get("analysis_intent", user_query)
        except json.JSONDecodeError:
            # Fallback if JSON parsing fails
            analysis_intent = result

        return {
            **state,
            "analysis_intent": analysis_intent,
            "current_analysis": result,
            "next_step": "context_tracking"
        }
