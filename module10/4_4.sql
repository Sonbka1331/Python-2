SELECT ROUND(
  (SELECT SUM(salary) FROM (SELECT salary FROM salaries ORDER BY salary DESC LIMIT (SELECT COUNT(*) * 0.1 FROM salaries)))
  /
  (SELECT SUM(salary) FROM (SELECT salary FROM salaries ORDER BY salary DESC LIMIT -1 OFFSET (SELECT COUNT(*) * 0.1 FROM salaries)))
  * 100,
  2
) AS F;
