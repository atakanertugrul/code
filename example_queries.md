# Example Queries for Sales Analysis Agent

This document provides example queries you can use with the Sales Analysis AI Agent.

## Basic Revenue Analysis

### Monthly Revenue
```
Show me total revenue by month
What are the monthly sales figures?
Give me a breakdown of sales by month
```

### City-wise Revenue
```
Show me revenue by city
Which cities generate the most sales?
What are the top performing cities?
```

### Product Revenue
```
Which products generate the most revenue?
Show me sales by product type
What are the best-selling products?
```

## Customer Analysis

### Customer Segmentation
```
Show me customer segments by revenue
Break down sales by customer age segment
What's the revenue distribution by customer gender?
```

### Top Customers
```
Who are my top 10 customers by revenue?
Show me the highest spending customers
Which customers have the most transactions?
```

### Customer Demographics
```
Show me sales by gender and age group
What's the breakdown by customer demographics?
Compare male vs female customers
```

## Product Analysis

### Product Performance
```
What are the top-selling product types?
Show me revenue by product category
Which product brands perform best?
```

### Material Analysis
```
What materials are most popular?
Show me sales by material type
Compare different materials by revenue
```

### Product Categories
```
Break down sales by category and subcategory
What are the top performing categories?
Show me product class distribution
```

## Channel Analysis

### Online vs Offline
```
Compare online vs offline sales
What's the revenue split between channels?
Show me online sales performance
Which channel performs better?
```

### Store Performance
```
Show me sales by store
Which stores generate the most revenue?
What are the top performing locations?
```

## Time-Based Analysis

### Trends
```
Show me sales trends over time
What's the monthly growth rate?
Compare this month to last month
```

### Specific Time Periods
```
Show me sales in January 2025
What were the sales in Q1?
Compare March vs April sales
```

### Daily Analysis
```
Show me sales by day of week
What are the best performing days?
Daily sales breakdown for January
```

## Discount Analysis

### Discount Impact
```
Show me the impact of discounts on revenue
Compare discounted vs non-discounted sales
What's the average discount rate?
```

### Season Analysis
```
Compare season vs off-season sales
Show me seasonal discount patterns
What's the revenue difference between seasons?
```

### Discount Effectiveness
```
Which discount rates drive the most volume?
Show me sales by discount type
Is there a correlation between discount and sales?
```

## Advanced Multi-Dimensional Analysis

### Combined Dimensions
```
Show me revenue by city and product type
Break down online sales by customer gender
Compare stores by product category performance
```

### Top-N Analysis
```
Top 5 products in each category
Top 10 customers by city
Best performing stores by month
```

### Comparative Analysis
```
Compare VAKKO vs VAKKORAMA brands
Istanbul vs Ankara sales comparison
Normal vs Outlet product performance
```

## Context-Aware Follow-up Queries

After running a query, you can ask follow-up questions:

### Initial Query
```
Show me total sales by city
```

### Follow-up Queries
```
Now break that down by product type
What about online sales only?
Show me the same for female customers
Filter for discount transactions
What about last month?
```

## Complex Business Questions

### Customer Insights
```
Which customer segments prefer which product types?
What's the average transaction value by customer age?
Show me repeat customer rates by city
```

### Product Strategy
```
Which products have the highest profit margins? (using net_amount and discount)
What's the product mix by store?
Show me cross-sell opportunities
```

### Regional Performance
```
Which cities have the highest average transaction value?
Compare regional preferences for products
Show me market penetration by city
```

### Inventory & Operations
```
Which materials are trending up or down?
Show me seasonal product performance
What's the sell-through rate by product class?
```

## Statistical Queries

### Aggregations
```
What's the average transaction value?
Show me total and average sales by category
Give me summary statistics for each month
```

### Distributions
```
Show me the distribution of transaction amounts
What's the customer count by segment?
Transaction frequency by customer
```

## Tips for Effective Queries

1. **Be Specific**: "Show me revenue by city" is better than "sales data"
2. **Use Natural Language**: Write as you would ask a colleague
3. **Build Context**: Start broad, then narrow down with follow-ups
4. **Combine Filters**: "Show me online sales for female customers in Istanbul"
5. **Ask for Comparisons**: "Compare X vs Y" or "Break down by Z"

## Interactive Commands

While in the agent:

- `history` - View your query history
- `schema` - View the database schema
- `exit` or `quit` - Exit the application

## Sample Analysis Session

```
📊 Your query: Show me total revenue by city

# Agent generates SQL and shows results in a table

📊 Your query: Which products sell best in Istanbul?

# Agent understands context and narrows down to Istanbul

📊 Your query: What about online vs offline?

# Agent adds channel comparison to the Istanbul product analysis

📊 Your query: Show me the same for Ankara

# Agent maintains the product + channel analysis but changes city
```

## Advanced SQL Features

The agent can handle:
- JOINs (if needed for complex queries)
- GROUP BY with multiple dimensions
- WHERE clauses with multiple conditions
- ORDER BY for sorting results
- Aggregate functions (SUM, AVG, COUNT, MAX, MIN)
- Date functions for time-based analysis
- CASE statements for conditional logic

## Notes

- All monetary values are in Turkish Lira (TL)
- Dates are in YYYY-MM-DD format
- Online transactions: f_online_tx = 1, Offline: f_online_tx = 0
- The agent validates all SQL for safety (no DELETE, UPDATE, DROP, etc.)
