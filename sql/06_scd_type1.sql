-- Data Engineering Practice
-- Topic: SCD Type 1
-- Scenario: Updating customer dimension records
--
-- SCD Type 1 overwrites the existing value.
-- Historical values are NOT retained.


-- 1. Identify new and changed customer records

SELECT
    s.CustomerID,
    s.CustomerName,
    s.Email,
    s.City
FROM StagingCustomer s
LEFT JOIN DimCustomer d
    ON s.CustomerID = d.CustomerID
WHERE d.CustomerID IS NULL
   OR ISNULL(s.CustomerName, '') <> ISNULL(d.CustomerName, '')
   OR ISNULL(s.Email, '') <> ISNULL(d.Email, '')
   OR ISNULL(s.City, '') <> ISNULL(d.City, '');


-- 2. Insert new customers

INSERT INTO DimCustomer
(
    CustomerID,
    CustomerName,
    Email,
    City
)
SELECT
    s.CustomerID,
    s.CustomerName,
    s.Email,
    s.City
FROM StagingCustomer s
LEFT JOIN DimCustomer d
    ON s.CustomerID = d.CustomerID
WHERE d.CustomerID IS NULL;


-- 3. Update existing customers

UPDATE d
SET
    d.CustomerName = s.CustomerName,
    d.Email = s.Email,
    d.City = s.City
FROM DimCustomer d
INNER JOIN StagingCustomer s
    ON d.CustomerID = s.CustomerID
WHERE ISNULL(d.CustomerName, '') <> ISNULL(s.CustomerName, '')
   OR ISNULL(d.Email, '') <> ISNULL(s.Email, '')
   OR ISNULL(d.City, '') <> ISNULL(s.City, '');


-- 4. SCD Type 1 using MERGE
-- MERGE can handle both INSERT and UPDATE
-- in a single operation.

MERGE DimCustomer AS Target
USING StagingCustomer AS Source
    ON Target.CustomerID = Source.CustomerID

WHEN MATCHED AND
(
       ISNULL(Target.CustomerName, '') <> ISNULL(Source.CustomerName, '')
    OR ISNULL(Target.Email, '') <> ISNULL(Source.Email, '')
    OR ISNULL(Target.City, '') <> ISNULL(Source.City, '')
)
THEN
    UPDATE SET
        Target.CustomerName = Source.CustomerName,
        Target.Email = Source.Email,
        Target.City = Source.City

WHEN NOT MATCHED BY TARGET
THEN
    INSERT
    (
        CustomerID,
        CustomerName,
        Email,
        City
    )
    VALUES
    (
        Source.CustomerID,
        Source.CustomerName,
        Source.Email,
        Source.City
    );


-- 5. Verify the dimension after the SCD Type 1 load

SELECT
    CustomerID,
    CustomerName,
    Email,
    City
FROM DimCustomer
ORDER BY CustomerID;