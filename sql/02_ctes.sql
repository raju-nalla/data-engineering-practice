-- Data Engineering Practice
-- Topic: Common Table Expressions (CTEs)
-- Scenario: Customer Order Analysis


-- 1. Calculate order count and total amount per customer
WITH CustomerOrderSummary AS
(
    SELECT
        CustomerID,
        COUNT(OrderID) AS OrderCount,
        COALESCE(SUM(Amount), 0) AS TotalOrderAmount
    FROM Orders
    GROUP BY CustomerID
)
SELECT
    CustomerID,
    OrderCount,
    TotalOrderAmount
FROM CustomerOrderSummary;


-- 2. Join the CTE with the Customers table
WITH CustomerOrderSummary AS
(
    SELECT
        CustomerID,
        COUNT(OrderID) AS OrderCount,
        COALESCE(SUM(Amount), 0) AS TotalOrderAmount
    FROM Orders
    GROUP BY CustomerID
)
SELECT
    c.CustomerID,
    c.CustomerName,
    COALESCE(s.OrderCount, 0) AS OrderCount,
    COALESCE(s.TotalOrderAmount, 0) AS TotalOrderAmount
FROM Customers c
LEFT JOIN CustomerOrderSummary s
    ON c.CustomerID = s.CustomerID;


-- 3. Find high-value customers
-- Customers whose total order amount is greater than 10000.
WITH CustomerOrderSummary AS
(
    SELECT
        CustomerID,
        SUM(Amount) AS TotalOrderAmount
    FROM Orders
    GROUP BY CustomerID
)
SELECT
    CustomerID,
    TotalOrderAmount
FROM CustomerOrderSummary
WHERE TotalOrderAmount > 10000;


-- 4. Find customers with more than 5 orders
WITH CustomerOrderSummary AS
(
    SELECT
        CustomerID,
        COUNT(OrderID) AS OrderCount
    FROM Orders
    GROUP BY CustomerID
)
SELECT
    CustomerID,
    OrderCount
FROM CustomerOrderSummary
WHERE OrderCount > 5;