SELECT
  CASE
    WHEN COUNT(*) % 2 = 0
    THEN (MAX(salary_sum.salary) + MIN(salary_sum.salary)) / 2
    ELSE AVG(salary_sum.salary)
  END AS median_salary
FROM
  (SELECT salary
   FROM salaries
   ORDER BY salary) AS salary_sum;
