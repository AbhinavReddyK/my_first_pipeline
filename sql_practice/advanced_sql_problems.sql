-- SQL Practice - Advanced Interview Problems
-- Topics: Window functions, CTEs, Self joins, 
-- Conditional aggregation, NULL handling
-- Database: PostgreSQL

-- ============================================
-- 1. Second Highest Salary
-- ============================================
SELECT (
    SELECT salary FROM (
        SELECT salary, DENSE_RANK() OVER (ORDER BY salary DESC) AS salary_rnk
        FROM employees
    ) AS ranked
    WHERE salary_rnk = 2
) AS SecondHighestSalary;

-- ============================================
-- 2. Top 2 Highest Paid Employees per Department
-- ============================================
WITH ranked AS (
    SELECT name, department, salary,
    DENSE_RANK() OVER (PARTITION BY department ORDER BY salary DESC) AS rnk
    FROM employees
)
SELECT * FROM ranked
WHERE rnk <= 2;

-- ============================================
-- 3. Employees Earning More Than Department Average
-- ============================================
WITH department_average AS (
    SELECT department, AVG(salary) AS avg_salary
    FROM employees
    GROUP BY department
),
salary_rank AS (
    SELECT e.id, e.name, e.department, e.salary, da.avg_salary,
    DENSE_RANK() OVER (PARTITION BY e.department ORDER BY e.salary DESC) AS rnk
    FROM employees e
    JOIN department_average da ON e.department = da.department
)
SELECT name, department, salary, avg_salary, rnk
FROM salary_rank
WHERE salary > avg_salary;

-- ============================================
-- 4. Employees Earning More Than Manager (Self Join)
-- ============================================
SELECT e.name AS Employee
FROM Employee e
JOIN Employee m ON e.managerId = m.id
WHERE e.salary > m.salary;

-- ============================================
-- 5. Combine Two Tables (LeetCode 175)
-- ============================================
SELECT p.firstName, p.lastName, a.city, a.state
FROM Person p
LEFT JOIN Address a ON p.personId = a.personId;

-- ============================================
-- 6. Customer Placing Largest Number of Orders
-- ============================================
SELECT customer_number
FROM Orders
GROUP BY customer_number
ORDER BY COUNT(order_number) DESC
LIMIT 1;

-- ============================================
-- 7. Monthly Transactions Report
-- ============================================
SELECT 
    TO_CHAR(trans_date, 'YYYY-MM') AS month,
    country,
    COUNT(*) AS trans_count,
    COUNT(CASE WHEN state = 'approved' THEN 1 END) AS approved_count,
    SUM(amount) AS trans_total_amount,
    COALESCE(SUM(CASE WHEN state = 'approved' THEN amount END), 0) AS approved_total_amount
FROM Transactions
GROUP BY month, country
ORDER BY month ASC;

-- ============================================
-- 8. Daily Active Users (30-Day Window)
-- ============================================
SELECT 
    activity_date AS day,
    COUNT(DISTINCT user_id) AS active_users
FROM Activity
WHERE activity_date BETWEEN '2019-06-28' AND '2019-07-27'
GROUP BY activity_date;
