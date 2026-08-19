-- Data Engineering Practice
-- Topic: Incremental Loading
-- Scenario: Loading only new or modified records from a source system

-- 1. Full load
-- Used during the initial pipeline execution.
SELECT
    OrderID,
    CustomerID,
    OrderDate,
    Amount,
    LastModifiedDate
FROM SourceOrders;


-- 2. Incremental load using a watermark
-- Assume @LastWatermark contains the timestamp
-- from the previous successful pipeline run.

DECLARE @LastWatermark DATETIME2 = '2026-01-01 00:00:00';

SELECT
    OrderID,
    CustomerID,
    OrderDate,
    Amount,
    LastModifiedDate
FROM SourceOrders
WHERE LastModifiedDate > @LastWatermark
  AND LastModifiedDate <= SYSUTCDATETIME();


-- 3. Capture the new maximum watermark
-- Store this value only after the target load succeeds.

SELECT
    MAX(LastModifiedDate) AS NewWatermark
FROM SourceOrders
WHERE LastModifiedDate > @LastWatermark
  AND LastModifiedDate <= SYSUTCDATETIME();


-- 4. Incremental load using an explicit upper boundary
-- Capturing the upper boundary at the beginning of a pipeline
-- makes the extraction deterministic.

DECLARE @LastWatermark DATETIME2 = '2026-01-01 00:00:00';
DECLARE @CurrentWatermark DATETIME2 = SYSUTCDATETIME();

SELECT
    OrderID,
    CustomerID,
    OrderDate,
    Amount,
    LastModifiedDate
FROM SourceOrders
WHERE LastModifiedDate > @LastWatermark
  AND LastModifiedDate <= @CurrentWatermark;


-- 5. Identify records that may have been updated
-- Incremental processing should capture both new and modified records.

SELECT
    OrderID,
    CustomerID,
    OrderDate,
    Amount,
    LastModifiedDate
FROM SourceOrders
WHERE LastModifiedDate > @LastWatermark
  AND LastModifiedDate <= @CurrentWatermark
ORDER BY LastModifiedDate;


-- 6. Example metadata update
-- In a real pipeline this would normally happen only
-- after the target load and validation complete successfully.

UPDATE PipelineWatermark
SET
    LastWatermark = @CurrentWatermark,
    UpdatedAt = SYSUTCDATETIME()
WHERE PipelineName = 'OrdersIncrementalLoad';