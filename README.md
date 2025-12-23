# Sales Analysis AI Agent

A multi-agent AI system built with LangGraph for natural language sales data analysis. The system converts natural language queries into SQL, executes them, and presents results in formatted tables.

## Features

- **Natural Language to SQL**: Convert plain language questions into SQL queries
- **Multi-Agent Architecture**: Three specialized agents working together:
  - **Analysis Understanding Agent**: Interprets user's analytical intent
  - **Context Tracking Agent**: Maintains context across multiple queries
  - **SQL Generation Agent**: Generates optimized SQL queries
- **Interactive CLI**: Easy-to-use command-line interface
- **Context-Aware**: Understands follow-up questions and builds on previous analyses
- **Formatted Results**: Beautiful table output with summary statistics
- **Turkish Retail Data**: Pre-loaded sample data from Turkish retail (VAKKO)

## Architecture

```
┌─────────────────────────────────────────────────────┐
│                  User Query (NL)                     │
└───────────────────┬─────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────┐
│         Analysis Understanding Agent                 │
│  (Understands what analysis user wants)             │
└───────────────────┬─────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────┐
│            Context Tracking Agent                    │
│  (Checks if query relates to previous analyses)     │
└───────────────────┬─────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────┐
│            SQL Generation Agent                      │
│  (Generates SQL queries from intent)                │
└───────────────────┬─────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────┐
│            Query Executor                            │
│  (Executes SQL and retrieves results)               │
└───────────────────┬─────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────┐
│            Results Formatter                         │
│  (Formats results as tables with statistics)        │
└─────────────────────────────────────────────────────┘
```

## Installation

1. **Clone the repository**:
```bash
git clone <repository-url>
cd <repository-name>
```

2. **Create a virtual environment**:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**:
```bash
cp .env.example .env
# Edit .env and add your OpenAI API key
```

## Configuration

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_openai_api_key_here
MODEL_NAME=gpt-4-turbo-preview
DATABASE_URL=sqlite:///sales_data.db
```

## Usage

### Interactive Mode

Run the agent in interactive mode:

```bash
python main.py
```

### Example Queries

Here are some example natural language queries you can try:

**Revenue Analysis**:
- "What are the total sales by month?"
- "Show me revenue by city"
- "Which products generated the most revenue?"

**Customer Analysis**:
- "Show me customer segments by revenue"
- "What's the breakdown by customer age and gender?"
- "Which customers made the most purchases?"

**Product Analysis**:
- "What are the top-selling product types?"
- "Show me sales by product category"
- "Which materials are most popular?"

**Channel Analysis**:
- "Compare online vs offline sales"
- "Show me store performance"
- "What's the revenue split between channels?"

**Time-Based Analysis**:
- "Show monthly trends"
- "Compare sales between months"
- "What were the best performing days?"

**Discount Analysis**:
- "Show me the impact of discounts on revenue"
- "Which discount rates are most common?"
- "Compare season vs off-season sales"

**Follow-up Queries** (Context-aware):
- After a query: "Break that down by gender"
- "Show me the same for online sales only"
- "What about the previous month?"

## Database Schema

The system uses a single `sales` table with the following structure:

### Sales Table

| Column | Type | Description |
|--------|------|-------------|
| `transaction_id` | INTEGER | Primary key (auto-increment) |
| `customer_id` | INTEGER | Customer identifier |
| `yearmonth` | TEXT | Year-month in YYYYMM format |
| `tx_date` | DATE | Transaction date (YYYY-MM-DD) |
| `net_amount` | DECIMAL | Transaction amount in TL |
| `discount_rate` | DECIMAL | Applied discount rate (0-1) |
| `season_discount` | TEXT | Discount type |
| `season_statues` | TEXT | Season status (Season/OffSeason) |
| `store_name` | TEXT | Store name |
| `f_online_tx` | INTEGER | Online flag (0=offline, 1=online) |
| `tx_city` | TEXT | Transaction city |
| `product_brand_name` | TEXT | Product brand (VAKKO, VAKKORAMA) |
| `product_type` | TEXT | Product type (Gömlek, Kazak, etc.) |
| `product_category` | TEXT | Category (Giyim, Aksesuar) |
| `product_subcategory` | TEXT | Subcategory (Üst Giyim, etc.) |
| `product_class` | TEXT | Class (Normal, Outlet) |
| `material` | TEXT | Material (Cotton, Silk, etc.) |
| `sap_mal_grubu_tanim` | TEXT | SAP material group |
| `customer_age_segment` | TEXT | Age segment (18-24, 25-34, etc.) |
| `customer_gender` | TEXT | Gender (Male, Female) |
| `customer_segment` | TEXT | Brand segment (Vakko, Vakko Butik) |

## Project Structure

```
.
├── data/
│   ├── schema.sql              # Database schema
│   └── sample_data.sql         # Sample sales data
├── src/
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── analysis_understanding_agent.py
│   │   ├── context_tracking_agent.py
│   │   └── sql_generation_agent.py
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── database.py         # Database management
│   │   └── formatters.py       # Result formatting
│   ├── __init__.py
│   ├── state.py                # State management
│   └── workflow.py             # LangGraph workflow
├── main.py                     # Application entry point
├── requirements.txt            # Python dependencies
├── .env.example               # Environment variables template
└── README.md                  # This file
```

## Best Practices Implemented

1. **Separation of Concerns**: Each agent has a single, well-defined responsibility
2. **Type Safety**: Using TypedDict for state management
3. **Database Indexing**: Optimized queries with proper indexes
4. **SQL Safety**: Query validation to prevent destructive operations
5. **Error Handling**: Comprehensive error handling throughout
6. **Context Management**: Maintains conversation history for follow-up queries
7. **Formatted Output**: Clean, readable table formatting with statistics
8. **Environment Configuration**: Secure API key management
9. **Modular Design**: Easy to extend with new agents or capabilities

## Advanced Features

### Context Awareness

The system remembers previous queries and can handle follow-up questions:

```
Query 1: "Show me total sales by city"
Query 2: "Now break that down by product type"  # Understands context
Query 3: "What about online sales only?"         # Builds on previous query
```

### Multiple Query Support

Complex analyses can generate multiple SQL queries:

```
Query: "Show me top customers and their favorite products"
# Generates 2 queries:
#   1. Top customers by revenue
#   2. Most purchased products per customer
```

### Summary Statistics

Automatically calculates and displays:
- Total rows returned
- Sum of numeric columns
- Average of numeric columns

## API Reference

### DatabaseManager

```python
from src.utils.database import DatabaseManager

db = DatabaseManager("sales_data.db")
db.initialize_database("data/schema.sql", "data/sample_data.sql")
df = db.execute_query("SELECT * FROM sales LIMIT 10")
schema = db.get_schema_info()
```

### SalesAnalysisWorkflow

```python
from src.workflow import SalesAnalysisWorkflow

workflow = SalesAnalysisWorkflow(db_manager, model_name="gpt-4-turbo-preview")
result = workflow.run("Show me sales by month")
print(result["formatted_output"])
```

## Troubleshooting

**API Key Error**:
```
Make sure OPENAI_API_KEY is set in your .env file
```

**Database Not Found**:
```
The database will be created automatically on first run
```

**Import Errors**:
```bash
pip install -r requirements.txt --upgrade
```

## Contributing

Contributions are welcome! Please follow these guidelines:
1. Fork the repository
2. Create a feature branch
3. Add tests for new features
4. Submit a pull request

## License

MIT License - See LICENSE file for details

## Support

For issues, questions, or contributions, please open an issue on GitHub.

---

Built with [LangGraph](https://github.com/langchain-ai/langgraph) and [LangChain](https://github.com/langchain-ai/langchain)
