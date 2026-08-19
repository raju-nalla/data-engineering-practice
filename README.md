# Data Engineering Practice

A structured repository for continuous Data Engineering interview preparation and hands-on practice.

This repository focuses on practical problems across SQL, PySpark, Databricks, ETL, Azure Data Engineering, and Data Quality.

---

# 🎯 Interview Practice Roadmap

The practice roadmap is designed around **Intermediate to Advanced Data Engineering interview scenarios**, with emphasis on problems commonly encountered in Data Engineer interviews.

---

# 🔥 SQL — Intermediate → Advanced

## Level 1 — Strong Intermediate

1. Employees earning more than their department average
2. Second-highest salary per department
3. Top 3 salaries per department
4. Customers with no orders
5. Customers who ordered in both January and February
6. Find duplicate customers
7. Remove duplicates while retaining the latest record
8. Most recent order per customer
9. First order per customer
10. Employees whose salary increased from previous year

---

## Level 2 — Window Functions

11. `ROW_NUMBER()` — latest record per customer
12. `RANK()` vs `DENSE_RANK()` — salary ranking
13. Running revenue by customer
14. Running monthly revenue
15. 7-day moving average
16. Previous transaction using `LAG()`
17. Next transaction using `LEAD()`
18. Difference between current and previous transaction
19. Percentage change from previous month
20. Top N products per category

> **Key Interview Focus:**  
> `ROW_NUMBER()`, `RANK()`, `DENSE_RANK()`, `LAG()`, `LEAD()`, running totals, moving averages, and partitioned analytics.

---

## Level 3 — CTE / Subquery / Business Logic

21. Customers whose spending is above average
22. Customers whose spending is above their city's average
23. Products never purchased
24. Employees with the same salary
25. Employees earning more than their manager
26. Find consecutive login days
27. Find users with 3+ consecutive active days
28. Find longest customer activity streak
29. Detect gaps in dates
30. Find missing dates from a transaction table

---

## Level 4 — Advanced Analytics

31. Gaps and Islands problem
32. Sessionization from user events
33. Customer retention by month
34. Cohort analysis
35. Monthly active users
36. Customer churn
37. Month-over-month revenue growth
38. Pareto analysis — customers contributing 80% revenue
39. Funnel conversion analysis
40. Product purchase sequence analysis

---

## Level 5 — Data Engineering SQL

41. SCD Type 1 implementation
42. SCD Type 2 implementation
43. CDC MERGE logic
44. Incremental load using watermark
45. Detect source-target mismatches
46. Reconciliation between two systems
47. Detect late-arriving records
48. Deduplicate CDC records
49. Build an idempotent load
50. Optimize a slow analytical query

### SQL Interview Focus

The SQL practice emphasizes:

- Complex joins
- CTEs
- Subqueries
- Window functions
- Ranking
- Aggregations
- Gaps and Islands
- Sessionization
- SCD Type 1 / Type 2
- CDC
- Incremental loading
- Data reconciliation
- Query optimization
- Analytical SQL

---

# 🔥 PySpark — Intermediate → Advanced

## DataFrame / Transformation

1. Filter invalid records
2. Handle nulls
3. Replace null values
4. Derive multiple columns
5. Conditional transformations with `when`
6. Parse dates
7. Extract year/month/day
8. Flatten nested JSON
9. Explode arrays
10. Normalize nested structures

---

## Joins

11. Inner join two DataFrames
12. Left anti join
13. Left semi join
14. Find unmatched records
15. Join three DataFrames
16. Broadcast join
17. Handle duplicate columns after joins
18. Join with different column names
19. Range-based join
20. Optimize a large-to-small join

---

## Window Functions

21. Latest record per customer
22. Second-highest transaction per customer
23. Top 3 transactions per customer
24. Running total
25. Moving average
26. Previous transaction using `lag`
27. Next transaction using `lead`
28. Detect consecutive events
29. Calculate time between events
30. Sessionization

---

## Aggregation

31. Daily revenue
32. Monthly customer revenue
33. Top customers per month
34. Rolling 7-day metrics
35. Distinct customer counts
36. Approximate distinct counts
37. Pivot data
38. Unpivot data
39. Aggregation after join
40. Group-level statistics

---

## Advanced / Performance

41. Repartition vs coalesce
42. Identify partition imbalance
43. Handle data skew
44. Salting a skewed join
45. Broadcast join vs shuffle join
46. Avoid unnecessary shuffles
47. Cache vs persist
48. Explain and analyze a Spark execution plan
49. Optimize a 500-GB transformation
50. Debug a Spark job running out of memory

### PySpark Interview Focus

The PySpark practice emphasizes:

- DataFrame transformations
- Joins
- Window functions
- Aggregations
- Partitioning
- Repartitioning
- `coalesce()`
- Broadcast joins
- Shuffle optimization
- Data skew
- Salting
- Caching and persistence
- Spark execution plans
- Memory optimization
- Large-scale data processing

---

# 📊 Practice Summary

| Technology | Problems | Difficulty |
|---|---:|---|
| SQL | 50 | Intermediate → Advanced |
| PySpark | 50 | Intermediate → Advanced |
| **Total** | **100** | **Interview Focused** |

---

# 🚀 Daily Practice Plan

The goal is to solve **5 problems per day**.

Each day will contain a combination of SQL and PySpark problems.

### Example

**Day 1**

- SQL #1 — Employees above department average
- SQL #11 — Latest record using `ROW_NUMBER()`
- SQL #21 — Spending above average
- PySpark #1 — Filter invalid records
- PySpark #11 — Inner join

**Day 2**

- SQL #2 — Second-highest salary
- SQL #12 — `RANK()` vs `DENSE_RANK()`
- SQL #26 — Consecutive login days
- PySpark #2 — Handle nulls
- PySpark #16 — Broadcast join

**Day 3**

- SQL #3 — Top 3 salaries
- SQL #15 — 7-day moving average
- SQL #31 — Gaps and Islands
- PySpark #21 — Latest record per customer
- PySpark #41 — Repartition vs coalesce

---

# 🧠 Solution Standards

Each solution should include:

### 1. Problem

Clearly describe the requirement.

### 2. Approach

Explain the reasoning before writing the code.

### 3. Solution

Provide the SQL or PySpark implementation.

### 4. Complexity

For example:

```text
Time Complexity: O(n)
Space Complexity: O(n)