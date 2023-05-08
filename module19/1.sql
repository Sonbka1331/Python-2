SELECT a.teacher_id, AVG(g.grade) AS average_grade
FROM assignments a, assignments_grades g
JOIN assignments_grades ON a.assisgnment_id = g.assisgnment_id
GROUP BY a.teacher_id
ORDER BY average_grade
LIMIT 1;