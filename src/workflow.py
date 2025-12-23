"""LangGraph workflow for sales analysis agent system."""

from langgraph.graph import StateGraph, END
from typing import Dict, Any
import pandas as pd

from .state import AgentState
from .agents import (
    AnalysisUnderstandingAgent,
    ContextTrackingAgent,
    SQLGenerationAgent
)
from .utils.database import DatabaseManager
from .utils.formatters import ResultFormatter


class SalesAnalysisWorkflow:
    """LangGraph workflow for multi-agent sales analysis."""

    def __init__(self, db_manager: DatabaseManager, model_name: str = "gpt-4-turbo-preview"):
        """Initialize the workflow.

        Args:
            db_manager: Database manager instance
            model_name: Name of the OpenAI model to use
        """
        self.db_manager = db_manager
        self.model_name = model_name

        # Initialize agents
        self.analysis_agent = AnalysisUnderstandingAgent(model_name)
        self.context_agent = ContextTrackingAgent(model_name)
        self.sql_agent = SQLGenerationAgent(model_name)
        self.formatter = ResultFormatter()

        # Build the graph
        self.graph = self._build_graph()

    def _build_graph(self) -> StateGraph:
        """Build the LangGraph workflow.

        Returns:
            Compiled StateGraph
        """
        # Create the graph
        workflow = StateGraph(AgentState)

        # Add nodes
        workflow.add_node("analysis_understanding", self._analysis_understanding_node)
        workflow.add_node("context_tracking", self._context_tracking_node)
        workflow.add_node("sql_generation", self._sql_generation_node)
        workflow.add_node("execute_queries", self._execute_queries_node)
        workflow.add_node("format_results", self._format_results_node)

        # Define edges
        workflow.set_entry_point("analysis_understanding")

        workflow.add_edge("analysis_understanding", "context_tracking")
        workflow.add_edge("context_tracking", "sql_generation")
        workflow.add_edge("sql_generation", "execute_queries")
        workflow.add_edge("execute_queries", "format_results")
        workflow.add_edge("format_results", END)

        # Compile the graph
        return workflow.compile()

    def _analysis_understanding_node(self, state: AgentState) -> AgentState:
        """Node for understanding analysis intent.

        Args:
            state: Current state

        Returns:
            Updated state
        """
        print("🔍 Understanding analysis intent...")
        return self.analysis_agent.analyze(state)

    def _context_tracking_node(self, state: AgentState) -> AgentState:
        """Node for tracking context.

        Args:
            state: Current state

        Returns:
            Updated state
        """
        print("🔗 Checking context with previous queries...")
        return self.context_agent.analyze(state)

    def _sql_generation_node(self, state: AgentState) -> AgentState:
        """Node for generating SQL queries.

        Args:
            state: Current state

        Returns:
            Updated state
        """
        print("💻 Generating SQL queries...")
        return self.sql_agent.generate(state)

    def _execute_queries_node(self, state: AgentState) -> AgentState:
        """Node for executing SQL queries.

        Args:
            state: Current state

        Returns:
            Updated state
        """
        print("⚡ Executing queries...")

        sql_queries = state.get("sql_queries", [])
        query_results = []

        for i, query in enumerate(sql_queries, 1):
            print(f"  Query {i}/{len(sql_queries)}...")

            # Validate query for safety
            if not self.sql_agent.validate_sql(query):
                state["error"] = f"Query {i} failed safety validation"
                state["next_step"] = "end"
                return state

            try:
                # Execute query
                result_df = self.db_manager.execute_query(query)

                query_results.append({
                    "query": query,
                    "result": result_df,
                    "row_count": len(result_df)
                })

            except Exception as e:
                state["error"] = f"Error executing query {i}: {str(e)}"
                state["next_step"] = "end"
                return state

        state["query_results"] = query_results
        state["next_step"] = "format_results"

        return state

    def _format_results_node(self, state: AgentState) -> AgentState:
        """Node for formatting results.

        Args:
            state: Current state

        Returns:
            Updated state
        """
        print("📊 Formatting results...")

        query_results = state.get("query_results", [])
        analysis_intent = state.get("analysis_intent", "")

        formatted_outputs = []

        # Format header
        formatted_outputs.append("=" * 80)
        formatted_outputs.append("SALES ANALYSIS RESULTS")
        formatted_outputs.append("=" * 80)
        formatted_outputs.append("")

        if analysis_intent:
            formatted_outputs.append(f"Analysis: {analysis_intent}")
            formatted_outputs.append("")

        # Format each query result
        for i, result in enumerate(query_results, 1):
            formatted_outputs.append(f"Query {i}:")
            formatted_outputs.append("-" * 80)

            # Show SQL
            formatted_outputs.append("SQL:")
            formatted_outputs.append(f"```sql\n{result['query']}\n```")
            formatted_outputs.append("")

            # Show results table
            formatted_outputs.append("Results:")
            result_df = result["result"]
            formatted_outputs.append(self.formatter.format_dataframe(result_df))
            formatted_outputs.append("")

            # Show summary
            formatted_outputs.append(f"Total Rows: {result['row_count']}")

            # Add statistics for numeric columns
            numeric_cols = result_df.select_dtypes(include=['int64', 'float64']).columns
            if len(numeric_cols) > 0:
                formatted_outputs.append("\nSummary Statistics:")
                for col in numeric_cols:
                    total = result_df[col].sum()
                    avg = result_df[col].mean()
                    formatted_outputs.append(f"  {col}: Total = {total:,.2f}, Average = {avg:,.2f}")

            formatted_outputs.append("")
            formatted_outputs.append("=" * 80)
            formatted_outputs.append("")

        state["formatted_output"] = "\n".join(formatted_outputs)
        state["next_step"] = "end"

        # Add to history
        if state.get("sql_queries"):
            new_query = {
                "description": analysis_intent,
                "sql_query": state["sql_queries"][0] if state["sql_queries"] else "",
                "result": query_results[0] if query_results else None
            }
            if "previous_queries" not in state:
                state["previous_queries"] = []
            state["previous_queries"].append(new_query)

        return state

    def run(self, user_query: str, previous_queries: list = None) -> Dict[str, Any]:
        """Run the workflow for a user query.

        Args:
            user_query: User's analysis request
            previous_queries: List of previous queries for context

        Returns:
            Final state with results
        """
        # Initialize state
        initial_state = {
            "user_query": user_query,
            "analysis_intent": "",
            "requires_context": False,
            "context_description": "",
            "previous_queries": previous_queries or [],
            "current_analysis": "",
            "sql_queries": [],
            "query_results": [],
            "schema_info": self.db_manager.get_schema_info(),
            "next_step": "analysis_understanding",
            "error": None,
            "formatted_output": ""
        }

        # Run the graph
        final_state = self.graph.invoke(initial_state)

        return final_state
