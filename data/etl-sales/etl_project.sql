-- use salesdb;

select * from sales_cleaned;

-- total sales 
SELECT SUM(Sales) AS Total_Sales
FROM sales_cleaned;

-- total profit 
SELECT SUM(Profit) AS Total_Profit
FROM sales_cleaned;

-- total cost 
SELECT SUM(Cost) AS Total_Cost
FROM sales_cleaned;

SELECT COUNT(*) AS Total_Orders
FROM sales_cleaned;

SELECT AVG(Sales) AS Average_Order_Value
FROM sales_cleaned;

-- profit margine 
SELECT 
    (SUM(Profit) / SUM(Sales) * 100) AS Profit_Margin
FROM sales_cleaned;

-- Region Analysis
SELECT 
    Region,
    SUM(Sales) AS Total_Sales
FROM sales_cleaned
GROUP BY Region
ORDER BY Total_Sales DESC;

-- profit by region 
SELECT 
    Region,
    SUM(Profit) AS Total_Profit
FROM sales_cleaned
GROUP BY Region
ORDER BY Total_Profit DESC;

-- refion profit margine  
SELECT 
    Region,
    (SUM(Profit) / SUM(Sales) * 100) AS Profit_Margin
FROM sales_cleaned
GROUP BY Region
ORDER BY Profit_Margin DESC;

-- product analysis
SELECT 
    Product,
    SUM(Sales) AS Total_Sales
FROM sales_cleaned
GROUP BY Product
ORDER BY Total_Sales DESC;

-- Profit by Product
SELECT 
    Product,
    SUM(Profit) AS Total_Profit
FROM sales_cleaned
GROUP BY Product
ORDER BY Total_Profit DESC;

-- Product Profit Margin 
SELECT 
    Product,
    SUM(Sales) AS Total_Sales,
    SUM(Profit) AS Total_Profit,
    ROUND(SUM(Profit) / SUM(Sales) * 100, 2) AS Profit_Margin
FROM sales_cleaned
GROUP BY Product
ORDER BY Profit_Margin DESC;

-- Customer Analysis 
-- Top 10 Customers by Sales
SELECT 
    Customer,
    SUM(Sales) AS Total_Sales
FROM sales_cleaned
GROUP BY Customer
ORDER BY Total_Sales DESC
LIMIT 10;

-- Top 10 Customers by Profit
SELECT 
    Customer,
    SUM(Profit) AS Total_Profit
FROM sales_cleaned
GROUP BY Customer
ORDER BY Total_Profit DESC
LIMIT 10; 

-- Customer Order Frequency
SELECT 
    Customer,
    COUNT(*) AS Number_of_Orders
FROM sales_cleaned
GROUP BY Customer
ORDER BY Number_of_Orders DESC;

-- Monthly Analysis
-- Monthly Sales
SELECT 
    Month,
    SUM(Sales) AS Total_Sales
FROM sales_cleaned
GROUP BY Month
ORDER BY Month desc;

-- Monthly Profit
SELECT 
    Month,
    SUM(Profit) AS Total_Profit
FROM sales_cleaned
GROUP BY Month
ORDER BY Month;

-- Monthly Profit Margin
SELECT 
    Month,
    ROUND(SUM(Profit) / SUM(Sales) * 100, 2) AS Profit_Margin
FROM sales_cleaned
GROUP BY Month
ORDER BY Month;

-- Important Business Queries 
-- Best Region + Product Combination
SELECT 
    Region,
    Product,
    SUM(Sales) AS Total_Sales,
    SUM(Profit) AS Total_Profit
FROM sales_cleaned
GROUP BY Region, Product
ORDER BY Total_Profit DESC;

-- High-Value Orders
SELECT 
    Order_ID,
    Customer,
    Product,
    Region,
    Sales,
    Profit
FROM sales_cleaned
WHERE Sales > 50000
ORDER BY Sales DESC;

-- Low-Profit Orders
SELECT 
    Order_ID,
    Customer,
    Product,
    Region,
    Sales,
    Profit
FROM sales_cleaned
WHERE Profit < 5000
ORDER BY Profit ASC;

-- Most Profitable Product in Each Region
SELECT 
    Region,
    Product,
    SUM(Profit) AS Total_Profit
FROM sales_cleaned
GROUP BY Region, Product
ORDER BY Region, Total_Profit DESC;