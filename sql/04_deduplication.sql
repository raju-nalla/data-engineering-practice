-- Data Engineering Practice
-- Topic: Data Deduplication
-- Scenario: Customer records arriving multiple times from source systems


-- 1. Identify duplicate customer records
-- CustomerID is the business key.
SELECT
    CustomerID,
    COUNT(*) AS RecordCount
FROM CustomerChanges
GROUP BY CustomerID
HAVING COUNT(*) > 1;


-- 2. Assign a row number to each version of a customer record
-- Latest UpdatedAt record gets ROW_NUMBER() = 1.
WITH RankedCustomers AS
(
    SELECT
        CustomerID,
        CustomerName,
        Email,
        Phone,
        UpdatedAt,
        ROW_NUMBER() OVER
        (
            PARTITION BY CustomerID
            ORDER BY UpdatedAt DESC
        ) AS RowNum
    FROM CustomerChanges
)
SELECT
    CustomerID,
    CustomerName,
    Email,
    Phone,
    UpdatedAt
FROM RankedCustomers
WHERE RowNum = 1;


-- 3. Identify records that should be removed
-- RowNum > 1 represents older duplicate records.
WITH RankedCustomers AS
(
    SELECT
        CustomerID,
        CustomerName,
        Email,
        Phone,
        UpdatedAt,
        ROW_NUMBER() OVER
        (
            PARTITION BY CustomerID
            ORDER BY UpdatedAt DESC
        ) AS RowNum
    FROM CustomerChanges
)
SELECT *
FROM RankedCustomers
WHERE RowNum > 1;


-- 4. Deduplicate while preserving the latest record
WITH RankedCustomers AS
(
    SELECT
        CustomerID,
        CustomerName,
        Email,
        Phone,
        UpdatedAt,
        ROW_NUMBER() OVER
        (
            PARTITION BY CustomerID
            ORDER BY UpdatedAt DESC
        ) AS RowNum
    FROM CustomerChanges
)
SELECT
    CustomerID,
    CustomerName,
    Email,
    Phone,
    UpdatedAt
FROM RankedCustomers
WHERE RowNum = 1;


-- 5. Deduplication using multiple business keys
-- Useful when CustomerID is not reliable or unavailable.
WITH RankedCustomers AS
(
    SELECT
        CustomerID,
        CustomerName,
        Email,
        Phone,
        UpdatedAt,
        ROW_NUMBER() OVER
        (
            PARTITION BY Email
            ORDER BY UpdatedAt DESC
        ) AS RowNum
    FROM CustomerChanges
)
SELECT
    CustomerID,
    CustomerName,
    Email,
    Phone,
    UpdatedAt
FROM RankedCustomers
WHERE RowNum = 1;