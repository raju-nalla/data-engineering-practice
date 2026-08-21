# SQL Problem 1 — Employees Above Department Average

## 🎯 Difficulty

Intermediate

## 🧩 Problem

You are given an `Employee` table containing employee information.

Write a SQL query to find all employees whose salary is **greater than the average salary of their respective department**.

The solution should return:

- Employee Name
- Department ID
- Salary

---

## 📋 Employee Table

### Table: `Employee`

| EmployeeID | EmployeeName | DepartmentID | Salary |
|---:|---|---:|---:|
| 101 | Arun | 10 | 60000 |
| 102 | Ravi | 10 | 80000 |
| 103 | Priya | 10 | 70000 |
| 104 | Kumar | 20 | 50000 |
| 105 | Sneha | 20 | 90000 |
| 106 | Anil | 20 | 60000 |

---

## 💡 Expected Result

| EmployeeName | DepartmentID | Salary |
|---|---:|---:|
| Ravi | 10 | 80000 |
| Sneha | 20 | 90000 |

## Solution

WITH EmployeeSalary AS
(
    SELECT
        EmployeeID,
        EmployeeName,
        DepartmentID,
        Salary,
        AVG(Salary) OVER (
            PARTITION BY DepartmentID
        ) AS Avg_Dept_Salary
    FROM Employee
)

SELECT
    EmployeeName,
    DepartmentID,
    Salary
FROM EmployeeSalary
WHERE Salary > Avg_Dept_Salary;

---

# 🧠 Approach

 We need to compare every employee's salary with the average salary of their department.

 A regular `GROUP BY` would produce only one row per department and would therefore lose the individual employee information.

 Instead, we can use a **window function**:

# ```sql
-  AVG(Salary) OVER (PARTITION BY DepartmentID)



# SQL Problem 2 — Latest Record Per Customer Using ROW_NUMBER()

## 🎯 Difficulty

Intermediate

## 📋 Orders Table

### Table: `Orders`

| OrderID | CustomerID | OrderDate | Amount |
|---:|---:|---|---:|
| 1001 | 101 | 2026-01-05 | 250 |
| 1002 | 102 | 2026-01-07 | 500 |
| 1003 | 101 | 2026-02-10 | 300 |
| 1004 | 103 | 2026-02-15 | 150 |
| 1005 | 102 | 2026-03-01 | 700 |
| 1006 | 101 | 2026-03-12 | 450 |
| 1007 | 103 | 2026-03-20 | 200 |

---

## 💡 Expected Result

| CustomerID | OrderID | OrderDate | Amount |
|---:|---:|---|---:|
| 101 | 1006 | 2026-03-12 | 450 |
| 102 | 1005 | 2026-03-01 | 700 |
| 103 | 1007 | 2026-03-20 | 200 |

## 🧩 Problem

You are given an `Orders` table containing customer order information.

Write a SQL query to find the **most recent order for each customer**.

The solution should return:

- Customer ID
- Order ID
- Order Date
- Order Amount


---

## 🧠 Interview Requirement

You should solve this problem using:

# ```sql
- ROW_NUMBER()

# Solution
 WITH CTE AS
(
    SELECT
        CustomerID,
        OrderID,
        OrderDate,
        OrderAmount,
        ROW_NUMBER() OVER
        (
            PARTITION BY CustomerID
            ORDER BY OrderDate DESC
        ) AS rn
    FROM Orders
)
SELECT
    CustomerID,
    OrderID,
    OrderDate,
    OrderAmount
FROM CTE
WHERE rn = 1;


# SQL Problem 3 — Customers Spending Above Average

## 🎯 Difficulty

Intermediate → Advanced

## 🧩 Problem

You are given an `Orders` table containing customer order information.

Write a SQL query to:

1. Calculate the **total spending for each customer**.
2. Calculate the **average spending across all customers**.
3. Return customers whose **total spending is greater than the average customer spending**.

The solution should return:

- Customer ID
- Total Spending

---

## 📋 Orders Table

### Table: `Orders`

| OrderID | CustomerID | OrderDate | Amount |
|---:|---:|---|---:|
| 1001 | 101 | 2026-01-05 | 200 |
| 1002 | 102 | 2026-01-07 | 500 |
| 1003 | 101 | 2026-01-15 | 300 |
| 1004 | 103 | 2026-01-20 | 100 |
| 1005 | 102 | 2026-02-05 | 400 |
| 1006 | 104 | 2026-02-10 | 800 |
| 1007 | 103 | 2026-02-15 | 200 |
| 1008 | 101 | 2026-02-20 | 400 |

---

## 💡 Expected Result

First calculate the total spending for each customer:

| CustomerID | Total Spending |
|---:|---:|
| 101 | 900 |
| 102 | 900 |
| 103 | 300 |
| 104 | 800 |

The average customer spending is:

# ```text
(900 + 900 + 300 + 800) / 4 = 725

## Solution

WITH CustomerSpending AS
(
    SELECT
        CustomerID,
        SUM(Amount) AS TotalSpending
    FROM Orders
    GROUP BY CustomerID
),
AverageSpending AS
(
    SELECT
        AVG(TotalSpending) AS AvgCustomerSpending
    FROM CustomerSpending
)
SELECT
    cs.CustomerID,
    cs.TotalSpending
FROM CustomerSpending cs
CROSS JOIN AverageSpending av
WHERE cs.TotalSpending > av.AvgCustomerSpending;
