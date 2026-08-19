from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parent.parent

exercises = [
    (
        "sql",
        "07_scd_type2.sql",
        "feat(sql): add SCD type 2 practice",
        """-- Data Engineering Practice
-- Topic: SCD Type 2
-- Preserve historical dimension changes.

MERGE DimCustomer AS Target
USING StagingCustomer AS Source
    ON Target.CustomerID = Source.CustomerID
   AND Target.IsCurrent = 1

WHEN MATCHED AND
(
       ISNULL(Target.CustomerName, '') <> ISNULL(Source.CustomerName, '')
    OR ISNULL(Target.Email, '') <> ISNULL(Source.Email, '')
    OR ISNULL(Target.City, '') <> ISNULL(Source.City, '')
)
THEN
    UPDATE SET
        Target.IsCurrent = 0,
        Target.EndDate = SYSUTCDATETIME()

WHEN NOT MATCHED BY TARGET
THEN
    INSERT
    (
        CustomerID,
        CustomerName,
        Email,
        City,
        StartDate,
        EndDate,
        IsCurrent
    )
    VALUES
    (
        Source.CustomerID,
        Source.CustomerName,
        Source.Email,
        Source.City,
        SYSUTCDATETIME(),
        NULL,
        1
    );

-- In production, a changed record is normally followed
-- by insertion of the new current version.
"""
    ),

    (
        "sql",
        "08_data_quality.sql",
        "feat(sql): add data quality checks",
        """-- Data Engineering Practice
-- Topic: Data Quality Checks

-- 1. Null business keys
SELECT *
FROM Orders
WHERE OrderID IS NULL
   OR CustomerID IS NULL;

-- 2. Invalid amounts
SELECT *
FROM Orders
WHERE Amount < 0;

-- 3. Duplicate order IDs
SELECT
    OrderID,
    COUNT(*) AS RecordCount
FROM Orders
GROUP BY OrderID
HAVING COUNT(*) > 1;

-- 4. Invalid dates
SELECT *
FROM Orders
WHERE OrderDate > SYSUTCDATETIME();

-- 5. Basic row-count validation
SELECT COUNT(*) AS TotalRecords
FROM Orders;
"""
    ),

    (
        "pyspark",
        "01_dataframe_transformations.py",
        "feat(pyspark): add dataframe transformations practice",
        """# Data Engineering Practice
# Topic: PySpark DataFrame Transformations

from pyspark.sql import functions as F

df = spark.read.parquet("/data/orders")

transformed_df = (
    df
    .select(
        "OrderID",
        "CustomerID",
        "OrderDate",
        "Amount"
    )
    .filter(F.col("Amount") > 0)
    .withColumn(
        "OrderDate",
        F.to_date("OrderDate")
    )
    .withColumn(
        "OrderYear",
        F.year("OrderDate")
    )
    .withColumn(
        "OrderMonth",
        F.month("OrderDate")
    )
)

transformed_df.show()
"""
    ),

    (
        "pyspark",
        "02_pyspark_joins.py",
        "feat(pyspark): add join optimization practice",
        """# Data Engineering Practice
# Topic: PySpark Joins

from pyspark.sql import functions as F

orders = spark.read.parquet("/data/orders")
customers = spark.read.parquet("/data/customers")

result = (
    orders.alias("o")
    .join(
        customers.alias("c"),
        F.col("o.CustomerID") == F.col("c.CustomerID"),
        "left"
    )
    .select(
        F.col("o.OrderID"),
        F.col("o.CustomerID"),
        F.col("o.Amount"),
        F.col("c.CustomerName")
    )
)

result.show()
"""
    ),

    (
        "databricks",
        "01_bronze_ingestion.py",
        "feat(databricks): add bronze ingestion practice",
        """# Databricks Practice
# Topic: Bronze Layer Ingestion

from pyspark.sql import functions as F

source_path = "/mnt/source/orders"
bronze_path = "/mnt/bronze/orders"

df = (
    spark.read
    .option("header", True)
    .option("inferSchema", True)
    .csv(source_path)
)

bronze_df = (
    df
    .withColumn("_ingestion_timestamp", F.current_timestamp())
    .withColumn("_source_file", F.input_file_name())
)

(
    bronze_df.write
    .format("delta")
    .mode("append")
    .save(bronze_path)
)
"""
    ),

    (
        "databricks",
        "02_delta_merge.py",
        "feat(databricks): add delta merge practice",
        """# Databricks Practice
# Topic: Delta Lake MERGE / Upsert

from delta.tables import DeltaTable

target = DeltaTable.forPath(
    spark,
    "/mnt/silver/customers"
)

source = spark.read.parquet(
    "/mnt/bronze/customers"
)

(
    target.alias("t")
    .merge(
        source.alias("s"),
        "t.CustomerID = s.CustomerID"
    )
    .whenMatchedUpdateAll()
    .whenNotMatchedInsertAll()
    .execute()
)
"""
    ),

    (
        "etl",
        "01_pipeline_watermark.py",
        "feat(etl): add pipeline watermark practice",
        """# Data Engineering Practice
# Topic: ETL Watermark Pattern

last_watermark = "2026-01-01 00:00:00"

query = f'''
SELECT *
FROM SourceOrders
WHERE LastModifiedDate > '{last_watermark}'
'''

# Pipeline pattern:
#
# 1. Read previous watermark
# 2. Extract changed records
# 3. Transform records
# 4. Load target
# 5. Validate successful load
# 6. Persist new watermark
#
# Never advance the watermark before
# the target load succeeds.
"""
    ),
]


def main():
    # Use UTC date so the workflow is deterministic.
    today = datetime.utcnow().date()
    index = (today.toordinal() - 1) % len(exercises)

    folder, filename, commit_message, content = exercises[index]

    target_dir = ROOT / folder
    target_dir.mkdir(parents=True, exist_ok=True)

    target_file = target_dir / filename

    # Don't overwrite an existing exercise.
    if target_file.exists():
        print(f"Exercise already exists: {target_file}")
        return

    target_file.write_text(
        content.strip() + "\n",
        encoding="utf-8"
    )

    print(f"Created: {target_file}")
    print(f"Commit: {commit_message}")


if __name__ == "__main__":
    main()