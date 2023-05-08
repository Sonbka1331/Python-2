SELECT student_id, AVG(grade) AS avg_grade
FROM assignments_grades
GROUP BY student_id
ORDER BY avg_grade DESC
LIMIT 10;
