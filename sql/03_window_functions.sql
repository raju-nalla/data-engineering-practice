-- Data Engineering Practice
-- Topic: SQL Window Functions
-- Scenario: Customer Order Analytics


-- 1. ROW_NUMBER()
-- Find the latest order for each customer.
WITH RankedOrders AS
(
    SELECT
        OrderID,
        CustomerID,
        OrderDate,
        Amount,
        ROW_NUMBER() OVER
        (
            PARTITION BY CustomerID
            ORDER BY OrderDate DESC, OrderID DESC
        ) AS RowNum
    FROM Orders
)
SELECT
    OrderID,
    CustomerID,
    OrderDate,
    Amount
FROM RankedOrders
WHERE RowNum = 1;


-- 2. RANK()
-- Rank customers based on their total order amount.
WITH CustomerSales AS
(
    SELECT
        CustomerID,
        SUM(Amount) AS TotalSales
    FROM Orders
    GROUP BY CustomerID
)
SELECT
    CustomerID,
    TotalSales,
    RANK() OVER
    (
        ORDER BY TotalSales DESC
    ) AS SalesRank
FROM CustomerSales;


-- 3. DENSE_RANK()
-- Rank customers without gaps when there are ties.
WITH CustomerSales AS
(
    SELECT
        CustomerID,
        SUM(Amount) AS TotalSales
    FROM Orders
    GROUP BY CustomerID
)
SELECT
    CustomerID,
    TotalSales,
    DENSE_RANK() OVER
    (
        ORDER BY TotalSales DESC
    ) AS SalesRank
FROM CustomerSales;


-- 4. LAG()
-- Compare each order amount with the customer's previous order.
SELECT
    OrderID,
    CustomerID,
    OrderDate,
    Amount,
    LAG(Amount) OVER
    (
        PARTITION BY CustomerID
        ORDER BY OrderDate, OrderID
    ) AS PreviousOrderAmount
FROM Orders;


-- 5. LEAD()
-- Find the next order date for each customer.
SELECT
    OrderID,
    CustomerID,
    OrderDate,
    LEAD(OrderDate) OVER
    (
        PARTITION BY CustomerID
        ORDER BY OrderDate, OrderID
    ) AS NextOrderDate
FROM Orders;


-- 6. Running total
-- Calculate cumulative customer spending over time.
SELECT
    CustomerID,
    OrderID,
    OrderDate,
    Amount,
    SUM(Amount) OVER
    (
        PARTITION BY CustomerID
        ORDER BY OrderDate, OrderID
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS RunningTotal
FROM Orders;