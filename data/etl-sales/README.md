# Sales-Performance-Business-Intelligence-End-to-End-ETL-Project
<img width="1145" height="657" alt="Screenshot 2026-09-03 183039" src="https://github.com/user-attachments/assets/685f2fc1-d5d3-4a63-b307-9b43239fd40c" />

Sales Performance & BI End-to-End ETL Project — Step-by-Step Notes
STAGE 1: Data Extraction & Cleaning (Python / Pandas / Jupyter Notebook)

Step 1 — Load raw data

Imported pandas
Loaded raw Excel file: sales_raw_500.xlsx
Initial shape: 520 rows × 7 columns (Order_ID, Order_Date, Customer, Region, Product, Sales, Cost)

Step 2 — Remove duplicate records

Ran df.drop_duplicates()
Rows dropped: 20 exact duplicates
Shape after: 500 rows

Step 3 — Fix and validate the date column

Converted Order_Date to proper datetime using pd.to_datetime(..., errors='coerce')
Any unparseable/invalid dates became NaT (Not a Time)

Step 4 — Remove invalid date records

Ran df.dropna(subset=['Order_Date'])
Rows dropped: 18 records with missing/invalid dates
Shape after: 482 rows (final clean dataset)

Step 5 — Feature engineering

Created profit column = Sales − Cost
Extracted Year from Order_Date
Extracted Month from Order_Date
Final dataset: 482 rows × 10 columns

Step 6 — Export clean data

Saved as sales_cleaned.csv
This file becomes the single source of truth for both SQL and Power BI
STAGE 2: Business Analysis (SQL)

Loaded sales_cleaned.csv into MySQL as table sales_cleaned. Wrote 18 queries across 6 analysis themes:

Step 7 — Overall KPIs

Total Sales (SUM(Sales))
Total Profit (SUM(Profit))
Total Cost (SUM(Cost))
Total Orders (COUNT(*))
Average Order Value (AVG(Sales))
Overall Profit Margin (SUM(Profit)/SUM(Sales)*100)

Step 8 — Region-level analysis

Total Sales by Region (ranked)
Total Profit by Region (ranked)
Profit Margin by Region (ranked)

Step 9 — Product-level analysis

Total Sales by Product (ranked)
Total Profit by Product (ranked)
Combined Sales + Profit + Margin by Product (ranked by margin)

Step 10 — Customer analysis

Top 10 Customers by Sales
Top 10 Customers by Profit
Customer Order Frequency (count of orders per customer)

Step 11 — Time-based analysis

Monthly Sales trend
Monthly Profit trend
Monthly Profit Margin trend

Step 12 — Business flag queries

Best Region + Product combination (by profit)
High-Value Orders (Sales > ₹50,000)
Low-Profit Orders (Profit < ₹5,000)
Most Profitable Product in each Region
STAGE 3: Dashboard Build (Power BI)

Step 13 — Connect data

Loaded sales_cleaned table into Power BI as the data model source

Step 14 — Build KPI summary cards

Card: Total Sales
Card: Total Cost
Card: Total Profit
Card: Total Orders
Card: Average Order Value

Step 15 — Build trend visual

Line chart: Total Sales & Total Profit trended by Month

Step 16 — Build comparison visuals

Column chart: Total Profit by Region
Clustered bar chart: Total Profit & Total Sales by Product
Pie chart: Profit Margin by Product

Step 17 — Build detail view

Pivot table: Region (rows) × Product (columns), values = Total Sales & Total Profit

Step 18 — Add interactivity

Slicer: Year
Slicer: Region
Slicer: Product
Summary of What This Project Demonstrates
End-to-end pipeline across 3 tools: Excel → Python → SQL → Power BI
Two distinct data-cleaning problems solved (duplicates + invalid dates), not just one
Feature engineering (derived Profit, Year, Month fields)
18 SQL queries covering KPI, regional, product, customer, time-series, and threshold-based analysis
A fully interactive BI dashboard with KPI cards, trend, comparison, and drill-down (pivot table) views, filterable by Year/Region/Product
Still Needed for Full Business Insights





