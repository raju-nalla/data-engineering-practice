-- Data Engineering Practice
-- Topic: SQL JOINs
-- Scenario: Customers and Orders

-- 1. INNER JOIN
-- Returns customers who have at least one order.
SELECT
    c.CustomerID,
    c.CustomerName,
    o.OrderID,
    o.OrderDate,
    o.Amount
FROM Customers c
INNER JOIN Orders o
    ON c.CustomerID = o.CustomerID;


-- 2. LEFT JOIN
-- Returns all customers, including customers without orders.
SELECT
    c.CustomerID,
    c.CustomerName,
    o.OrderID,
    o.OrderDate,
    o.Amount
FROM Customers c
LEFT JOIN Orders o
    ON c.CustomerID = o.CustomerID;


-- 3. Find customers who have never placed an order.
SELECT
    c.CustomerID,
    c.CustomerName
FROM Customers c
LEFT JOIN Orders o
    ON c.CustomerID = o.CustomerID
WHERE o.OrderID IS NULL;


-- 4. Calculate total order amount per customer.
SELECT
    c.CustomerID,
    c.CustomerName,
    COUNT(o.OrderID) AS OrderCount,
    COALESCE(SUM(o.Amount), 0) AS TotalOrderAmount
FROM Customers c
LEFT JOIN Orders o
    ON c.CustomerID = o.CustomerID
GROUP BY
    c.CustomerID,
    c.CustomerName;