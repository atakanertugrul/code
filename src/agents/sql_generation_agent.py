"""Agent for generating SQL queries from analysis intent."""

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from typing import Dict, Any, List
import json
import re


class SQLGenerationAgent:
    """Agent that generates SQL queries based on analysis requirements."""

    def __init__(self, model_name: str = "gpt-4-turbo-preview"):
        """Initialize the SQL generation agent.

        Args:
            model_name: Name of the OpenAI model to use
        """
        self.llm = ChatOpenAI(model=model_name, temperature=0)

        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert SQL developer specializing in sales analytics.

Database Schema:
{schema_info}

Analysis Intent:
{analysis_intent}

Context Information:
{context_info}

Previous Queries (for reference):
{previous_queries}

Generate SQL queries to fulfill the analysis requirements. Follow these guidelines:
1. Generate clean, well-formatted SQL queries
2. Use appropriate JOINs when multiple tables are needed
3. Include proper aggregations (SUM, AVG, COUNT, etc.) as needed
4. Add GROUP BY clauses for aggregations
5. Use ORDER BY to sort results meaningfully
6. Add appropriate WHERE clauses for filtering
7. If multiple queries are needed for complete analysis, generate all of them
8. Use descriptive column aliases for calculated fields

Respond in JSON format:
{{
    "queries": [
        {{
            "description": "What this query does",
            "sql": "The SQL query",
            "purpose": "Why this query is needed"
        }}
    ],
    "notes": "Any additional notes about the queries"
}}

IMPORTANT: Generate valid SQLite queries. Return ONLY the JSON response, no additional text."""),
            ("user", "Generate SQL queries for: {user_query}")
        ])

        self.chain = self.prompt | self.llm | StrOutputParser()

    def generate(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Generate SQL queries based on analysis intent.

        Args:
            state: Current agent state

        Returns:
            Updated state with SQL queries
        """
        user_query = state["user_query"]
        analysis_intent = state.get("analysis_intent", "")
        schema_info = state.get("schema_info", "")
        requires_context = state.get("requires_context", False)
        context_description = state.get("context_description", "")
        previous_queries = state.get("previous_queries", [])

        # Build context info
        context_info = ""
        if requires_context and context_description:
            context_info = f"This query relates to previous analysis: {context_description}\n"

        # Build previous queries summary
        prev_queries_text = ""
        if previous_queries and requires_context:
            for i, query in enumerate(previous_queries[-3:]):
                prev_queries_text += f"{i+1}. {query.get('description', 'N/A')}\n"
                prev_queries_text += f"   SQL: {query.get('sql_query', 'N/A')}\n\n"

        # Generate SQL queries
        result = self.chain.invoke({
            "user_query": user_query,
            "analysis_intent": analysis_intent,
            "schema_info": schema_info,
            "context_info": context_info,
            "previous_queries": prev_queries_text or "None"
        })

        # Parse JSON response
        try:
            # Extract JSON from markdown code blocks if present
            json_match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', result, re.DOTALL)
            if json_match:
                result = json_match.group(1)

            sql_data = json.loads(result)
            queries = sql_data.get("queries", [])

            # Extract SQL queries
            sql_queries = [q["sql"] for q in queries]

            return {
                **state,
                "sql_queries": sql_queries,
                "next_step": "execute_queries"
            }

        except (json.JSONDecodeError, KeyError) as e:
            # Try to extract SQL from plain text response
            sql_pattern = r'SELECT\s+.*?(?:;|$)'
            found_queries = re.findall(sql_pattern, result, re.DOTALL | re.IGNORECASE)

            if found_queries:
                return {
                    **state,
                    "sql_queries": found_queries,
                    "next_step": "execute_queries"
                }
            else:
                return {
                    **state,
                    "error": f"Failed to generate SQL queries: {str(e)}",
                    "next_step": "end"
                }

    @staticmethod
    def validate_sql(query: str) -> bool:
        """Validate SQL query for safety.

        Args:
            query: SQL query to validate

        Returns:
            True if query is safe, False otherwise
        """
        # Basic safety checks
        dangerous_keywords = ['DROP', 'DELETE', 'UPDATE', 'INSERT', 'ALTER', 'CREATE']
        query_upper = query.upper()

        for keyword in dangerous_keywords:
            if keyword in query_upper:
                return False

        return True
