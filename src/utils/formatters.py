"""Formatting utilities for displaying results."""

import pandas as pd
from tabulate import tabulate
from typing import Any, Dict, List


class ResultFormatter:
    """Formats query results for display."""

    @staticmethod
    def format_dataframe(df: pd.DataFrame, tablefmt: str = "grid") -> str:
        """Format DataFrame as a table.

        Args:
            df: DataFrame to format
            tablefmt: Table format style (grid, simple, pipe, etc.)

        Returns:
            Formatted table string
        """
        if df.empty:
            return "No results found."

        return tabulate(df, headers='keys', tablefmt=tablefmt, showindex=False)

    @staticmethod
    def format_analysis_result(
        query: str,
        result_df: pd.DataFrame,
        analysis_description: str = ""
    ) -> str:
        """Format a complete analysis result.

        Args:
            query: The SQL query that was executed
            result_df: Query results
            analysis_description: Description of the analysis

        Returns:
            Formatted analysis result
        """
        output = []

        if analysis_description:
            output.append(f"Analysis: {analysis_description}")
            output.append("")

        output.append("SQL Query:")
        output.append(f"```sql\n{query}\n```")
        output.append("")

        output.append("Results:")
        output.append(ResultFormatter.format_dataframe(result_df))
        output.append("")

        # Add summary statistics if numerical data
        numeric_cols = result_df.select_dtypes(include=['int64', 'float64']).columns
        if len(numeric_cols) > 0:
            output.append("Summary Statistics:")
            output.append(f"Total Rows: {len(result_df)}")
            for col in numeric_cols:
                if col in result_df.columns:
                    output.append(f"  {col}: Sum = {result_df[col].sum():.2f}, "
                                f"Avg = {result_df[col].mean():.2f}")

        return "\n".join(output)
