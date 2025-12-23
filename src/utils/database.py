"""Database utilities for the sales analysis system."""

import sqlite3
from pathlib import Path
from typing import List, Dict, Any
import pandas as pd


class DatabaseManager:
    """Manages database connections and operations."""

    def __init__(self, db_path: str = "sales_data.db"):
        """Initialize database manager.

        Args:
            db_path: Path to the SQLite database file
        """
        self.db_path = db_path
        self.connection = None

    def connect(self) -> sqlite3.Connection:
        """Establish database connection."""
        if self.connection is None:
            self.connection = sqlite3.connect(self.db_path)
            self.connection.row_factory = sqlite3.Row
        return self.connection

    def close(self):
        """Close database connection."""
        if self.connection:
            self.connection.close()
            self.connection = None

    def initialize_database(self, schema_path: str, data_path: str):
        """Initialize database with schema and sample data.

        Args:
            schema_path: Path to SQL schema file
            data_path: Path to SQL data file
        """
        conn = self.connect()
        cursor = conn.cursor()

        # Read and execute schema
        with open(schema_path, 'r') as f:
            schema_sql = f.read()
            cursor.executescript(schema_sql)

        # Read and execute data
        with open(data_path, 'r') as f:
            data_sql = f.read()
            cursor.executescript(data_sql)

        conn.commit()
        print(f"Database initialized successfully at {self.db_path}")

    def execute_query(self, query: str) -> pd.DataFrame:
        """Execute SQL query and return results as DataFrame.

        Args:
            query: SQL query to execute

        Returns:
            DataFrame containing query results
        """
        conn = self.connect()
        try:
            df = pd.read_sql_query(query, conn)
            return df
        except Exception as e:
            raise Exception(f"Error executing query: {str(e)}")

    def get_schema_info(self) -> str:
        """Get database schema information.

        Returns:
            String containing schema information
        """
        conn = self.connect()
        cursor = conn.cursor()

        # Get all tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()

        schema_info = "Database Schema:\n\n"

        for table in tables:
            table_name = table[0]
            schema_info += f"Table: {table_name}\n"

            # Get column information
            cursor.execute(f"PRAGMA table_info({table_name});")
            columns = cursor.fetchall()

            for col in columns:
                col_name = col[1]
                col_type = col[2]
                not_null = "NOT NULL" if col[3] else ""
                pk = "PRIMARY KEY" if col[5] else ""
                schema_info += f"  - {col_name} {col_type} {not_null} {pk}\n"

            schema_info += "\n"

        return schema_info

    def get_sample_data(self, table_name: str, limit: int = 5) -> pd.DataFrame:
        """Get sample data from a table.

        Args:
            table_name: Name of the table
            limit: Number of rows to return

        Returns:
            DataFrame containing sample data
        """
        query = f"SELECT * FROM {table_name} LIMIT {limit}"
        return self.execute_query(query)
