from pathlib import Path


# ============================================================
# Configuration
# ============================================================

ROOT = Path(__file__).resolve().parent.parent


# ============================================================
# Exercise List
# ============================================================
# Add new exercises ONLY inside this list.
#
# Each exercise contains:
# 1. Folder
# 2. File name
# 3. Commit message
# 4. File content
# ============================================================

exercises = [

    # --------------------------------------------------------
    # SQL
    # --------------------------------------------------------

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
        "sql",
        "09_query_optimization.sql",
        "feat(sql): add query optimization practice",
        """-- Data Engineering Practice
-- Topic: SQL Query Optimization

-- Example query
SELECT
    CustomerID,
    COUNT(*) AS OrderCount,
    SUM(Amount) AS TotalAmount
FROM Orders
GROUP BY CustomerID
ORDER BY TotalAmount DESC;

-- Optimization ideas:
-- 1. Check execution plan
-- 2. Review indexes
-- 3. Avoid SELECT *
-- 4. Filter early
-- 5. Check table statistics
"""
    ),

    (
        "sql",
        "10_stored_procedure.sql",
        "feat(sql): add stored procedure practice",
        """-- Data Engineering Practice
-- Topic: Stored Procedure

CREATE PROCEDURE GetCustomerOrders
    @CustomerID INT
AS
BEGIN

    SELECT
        OrderID,
        CustomerID,
        OrderDate,
        Amount
    FROM Orders
    WHERE CustomerID = @CustomerID
    ORDER BY OrderDate DESC;

END;
"""
    ),


    # --------------------------------------------------------
    # PySpark
    # --------------------------------------------------------

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
        "pyspark",
        "03_window_functions.py",
        "feat(pyspark): add window functions practice",
        """# Data Engineering Practice
# Topic: PySpark Window Functions

from pyspark.sql import functions as F
from pyspark.sql.window import Window

window_spec = (
    Window
    .partitionBy("CustomerID")
    .orderBy(F.col("OrderDate"))
)

result = (
    orders
    .withColumn(
        "PreviousAmount",
        F.lag("Amount").over(window_spec)
    )
    .withColumn(
        "RunningTotal",
        F.sum("Amount").over(window_spec)
    )
)

result.show()
"""
    ),

    (
        "pyspark",
        "04_deduplication.py",
        "feat(pyspark): add deduplication practice",
        """# Data Engineering Practice
# Topic: PySpark Deduplication

from pyspark.sql import functions as F
from pyspark.sql.window import Window

window_spec = (
    Window
    .partitionBy("CustomerID")
    .orderBy(F.col("UpdatedAt").desc())
)

deduplicated_df = (
    df
    .withColumn(
        "row_num",
        F.row_number().over(window_spec)
    )
    .filter(F.col("row_num") == 1)
    .drop("row_num")
)

deduplicated_df.show()
"""
    ),


    # --------------------------------------------------------
    # Databricks
    # --------------------------------------------------------

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
        "databricks",
        "03_incremental_load.py",
        "feat(databricks): add incremental loading practice",
        """# Databricks Practice
# Topic: Incremental Loading

from pyspark.sql import functions as F

last_watermark = "2026-01-01 00:00:00"

df = spark.read.parquet("/mnt/bronze/orders")

incremental_df = (
    df
    .filter(
        F.col("LastModifiedDate") > last_watermark
    )
)

incremental_df.show()
"""
    ),

    (
        "databricks",
        "04_spark_optimization.py",
        "feat(databricks): add spark optimization practice",
        """# Databricks Practice
# Topic: Spark Optimization

from pyspark.sql import functions as F

result = (
    orders
    .repartition("CustomerID")
    .filter(F.col("Amount") > 0)
    .select(
        "OrderID",
        "CustomerID",
        "Amount"
    )
)

result.explain(True)
"""
    ),


    # --------------------------------------------------------
    # ETL
    # --------------------------------------------------------

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

    (
        "etl",
        "02_cdc_pipeline.py",
        "feat(etl): add CDC pipeline practice",
        """# Data Engineering Practice
# Topic: Change Data Capture

# CDC pipeline pattern:
#
# 1. Read CDC changes
# 2. Identify INSERT / UPDATE / DELETE
# 3. Transform records
# 4. Apply changes to target
# 5. Validate counts
# 6. Store processing watermark

cdc_query = '''
SELECT
    CustomerID,
    Operation,
    LastModifiedDate
FROM CustomerChanges
WHERE LastModifiedDate > @LastWatermark
'''
"""
    ),

    (
        "etl",
        "03_data_validation.py",
        "feat(etl): add pipeline validation practice",
        """# Data Engineering Practice
# Topic: ETL Validation

def validate_counts(source_count, target_count):
    if source_count != target_count:
        raise ValueError(
            f"Count mismatch: "
            f"source={source_count}, "
            f"target={target_count}"
        )

    print("Validation successful")
"""
    ),
]


# ============================================================
# Find the next exercise
# ============================================================

def find_next_exercise():

    for exercise in exercises:

        folder, filename, commit_message, content = exercise

        target_file = ROOT / folder / filename

        if not target_file.exists():
            return exercise

    return None


# ============================================================
# Create next exercise
# ============================================================

def main():

    exercise = find_next_exercise()

    if exercise is None:

        print("========================================")
        print("All exercises have been completed.")
        print("Nothing to commit.")
        print("========================================")

        return

    folder, filename, commit_message, content = exercise

    target_dir = ROOT / folder

    target_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    target_file = target_dir / filename

    target_file.write_text(
        content.strip() + "\n",
        encoding="utf-8"
    )

    print("========================================")
    print("New exercise created")
    print("========================================")

    print(f"Folder : {folder}")
    print(f"File   : {filename}")
    print(f"Commit : {commit_message}")

    print("========================================")


# ============================================================
# Entry Point
# ============================================================

if __name__ == "__main__":
    main()