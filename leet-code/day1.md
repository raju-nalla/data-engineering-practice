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

```sql
AVG(Salary) OVER (PARTITION BY DepartmentID)


