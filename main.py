"""Main entry point for the Sales Analysis Agent System."""

import os
from pathlib import Path
from dotenv import load_dotenv

from src.utils.database import DatabaseManager
from src.workflow import SalesAnalysisWorkflow


def initialize_database():
    """Initialize the database with schema and sample data."""
    db_manager = DatabaseManager("sales_data.db")

    # Check if database needs initialization
    db_path = Path("sales_data.db")
    if not db_path.exists():
        print("📦 Initializing database...")
        schema_path = "data/schema.sql"
        data_path = "data/sample_data.sql"

        db_manager.initialize_database(schema_path, data_path)
        print("✅ Database initialized successfully!\n")
    else:
        print("✅ Database already exists.\n")

    return db_manager


def run_interactive_mode(workflow: SalesAnalysisWorkflow):
    """Run the agent in interactive mode.

    Args:
        workflow: The sales analysis workflow instance
    """
    print("=" * 80)
    print("SALES ANALYSIS AGENT - Interactive Mode")
    print("=" * 80)
    print("\nType your analysis queries in natural language.")
    print("Type 'exit' or 'quit' to end the session.")
    print("Type 'history' to see previous queries.")
    print("Type 'schema' to see database schema.\n")
    print("=" * 80)
    print()

    # Store query history
    query_history = []

    while True:
        try:
            # Get user input
            user_input = input("📊 Your query: ").strip()

            if not user_input:
                continue

            # Handle special commands
            if user_input.lower() in ['exit', 'quit']:
                print("\n👋 Thanks for using Sales Analysis Agent!")
                break

            if user_input.lower() == 'history':
                if not query_history:
                    print("No previous queries.\n")
                else:
                    print("\n📜 Query History:")
                    print("-" * 80)
                    for i, query in enumerate(query_history, 1):
                        print(f"{i}. {query['description']}")
                    print()
                continue

            if user_input.lower() == 'schema':
                schema_info = workflow.db_manager.get_schema_info()
                print("\n" + schema_info)
                continue

            # Run the workflow
            print()
            result = workflow.run(user_input, query_history)

            # Check for errors
            if result.get("error"):
                print(f"\n❌ Error: {result['error']}\n")
                continue

            # Display results
            print("\n" + result.get("formatted_output", "No results"))

            # Update history
            if result.get("previous_queries"):
                query_history = result["previous_queries"]

        except KeyboardInterrupt:
            print("\n\n👋 Thanks for using Sales Analysis Agent!")
            break
        except Exception as e:
            print(f"\n❌ Unexpected error: {str(e)}\n")


def run_single_query(workflow: SalesAnalysisWorkflow, query: str):
    """Run a single query and display results.

    Args:
        workflow: The sales analysis workflow instance
        query: The analysis query
    """
    print(f"\n📊 Query: {query}\n")

    result = workflow.run(query)

    if result.get("error"):
        print(f"\n❌ Error: {result['error']}\n")
    else:
        print("\n" + result.get("formatted_output", "No results"))


def main():
    """Main function."""
    # Load environment variables
    load_dotenv()

    # Check for API key
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ Error: OPENAI_API_KEY not found in environment variables.")
        print("Please create a .env file with your OpenAI API key.")
        print("See .env.example for reference.")
        return

    # Initialize database
    db_manager = initialize_database()

    # Get model name from environment
    model_name = os.getenv("MODEL_NAME", "gpt-4-turbo-preview")

    # Initialize workflow
    print(f"🚀 Initializing Sales Analysis Agent (Model: {model_name})...\n")
    workflow = SalesAnalysisWorkflow(db_manager, model_name)

    # Run in interactive mode
    run_interactive_mode(workflow)

    # Close database connection
    db_manager.close()


if __name__ == "__main__":
    main()
