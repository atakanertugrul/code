"""State management for the LangGraph workflow."""

from typing import TypedDict, List, Optional, Dict, Any
from typing_extensions import Annotated
import operator


class AnalysisQuery(TypedDict):
    """Represents a single analysis query."""
    description: str
    sql_query: str
    result: Optional[Any]


class AgentState(TypedDict):
    """State for the sales analysis agent system."""

    # User input
    user_query: str

    # Analysis understanding
    analysis_intent: str
    requires_context: bool
    context_description: str

    # Query history
    previous_queries: Annotated[List[AnalysisQuery], operator.add]

    # Current analysis
    current_analysis: str
    sql_queries: Annotated[List[str], operator.add]

    # Results
    query_results: Annotated[List[Dict[str, Any]], operator.add]

    # Database schema
    schema_info: str

    # Control flow
    next_step: str
    error: Optional[str]

    # Final output
    formatted_output: str
