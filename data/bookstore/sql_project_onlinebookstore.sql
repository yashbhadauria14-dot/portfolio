-- Create Database

-- CREATE DATABASE OnlineBookstore;
 use OnlineBookstore;
-- Switch to the database

SELECT * FROM Books;
SELECT * FROM Customers;
SELECT * FROM Orders;


-- 1) Retrieve all books in the "Fiction" genre:
select * from books
where Genre = 'fiction';

-- 2) Find books published after the year 1950:
select * from books
where Published_Year>1950;

-- 3) List all customers from the Canada:
select * from customers
where country = 'canada';

-- 4) Show orders placed in November 2023:
select * from orders
where order_date between '2023-11-1' and '2023-11-30';

-- 5) Retrieve the total stock of books available:
select sum(stock) as total_stock
from books;

-- 6) Find the details of the most expensive book:
select * from books
order by price desc
limit 1;

-- 7) Show all customers who ordered more than 1 quantity of a book:
select * from orders
where quantity>1;

-- 8) Retrieve all orders where the total amount exceeds $20:
select * from orders
where total_amount > 20;

-- 9) List all genres available in the Books table:
select distinct genre from books;

-- 10) Find the book with the lowest stock:
select * from books
order by stock
limit 1;

-- 11) Calculate the total revenue generated from all orders:
select sum(total_amount) as revenue from orders;

-- Advance Questions : 

-- 1) Retrieve the total number of books sold for each genre:
select b.genre, sum(o.quantity) as books_sold
from orders o
join books b on o.Book_ID = b.book_id
group by b.Genre;

-- 2) Find the average price of books in the "Fantasy" genre:
select avg(price) as avg_price from books
where Genre = 'fantasy';

-- 3) List customers who have placed at least 2 orders:
select o.customer_id, c.name, count(o.order_id) as total_orders
from orders o
join customers c on o.customer_id = c.customer_id
group by customer_id , c.name
having count(order_id)>=2; 

-- 4) Find the most frequently ordered book:
select o.Book_ID, b.title, count(o.order_id) as order_count
from orders o
join books b on o.Book_ID = b.Book_ID
group by o.Book_ID, b.title
order by order_count desc 
limit 1;

-- 5) Show the top 3 most expensive books of 'Fantasy' Genre :
select * from books
where Genre = 'fantasy' 
order by price desc limit 3;

-- 6) Retrieve the total quantity of books sold by each author:
select b.author, sum(o.quantity) as total_orders
from orders o 
join books b on o.book_id = b.book_id
group by b.author;

-- 7) List the cities where customers who spent over $30 are located:
select distinct c.city, o.total_amount
from orders o
join customers c on o.customer_id = c.customer_id
where o.total_amount> 30; 

-- 8) Find the customer who spent the most on orders:
select c.name, sum(o.total_amount) as total
from orders o
join customers c on o.customer_id = c.customer_id
group by c.name
order by total desc limit 1

-- windows function and CTE

-- 1) Row Number for each order by customer by 1st purchase and 2nd purchase date vise
SELECT Customer_ID, Order_ID, Order_Date,
ROW_NUMBER() OVER(PARTITION BY Customer_ID ORDER BY Order_Date) AS Order_No
FROM Orders;

-- 2) ranks customers based on how much money they have spent
SELECT customer_ID, SUM(Total_Amount) AS Total_Spent,
DENSE_RANK() OVER (ORDER BY SUM(Total_Amount) DESC) AS Ranks
FROM Orders
GROUP BY Customer_ID;

-- 3) Top 3 Orders Per Customer
SELECT * FROM
(SELECT *, ROW_NUMBER() OVER(PARTITION BY Customer_ID ORDER BY Total_Amount DESC) AS rn
FROM Orders) t
WHERE rn <= 3;

-- 4) Customers Spending Above Average
WITH CustomerSales AS
(SELECT Customer_ID, SUM(Total_Amount) AS TotalSales FROM Orders
GROUP BY Customer_ID)
SELECT *
FROM CustomerSales
WHERE TotalSales >
(SELECT AVG(TotalSales)FROM CustomerSales);







