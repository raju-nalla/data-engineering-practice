# Data Engineering Practice
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
