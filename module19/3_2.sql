SELECT s.full_name AS student_name, AVG(ag.grade) AS average_grade
FROM students AS s
INNER JOIN assignments_grades AS ag ON s.student_id = ag.student_id
INNER JOIN assignments AS a ON ag.assisgnment_id = a.assisgnment_id
INNER JOIN (
  SELECT a.teacher_id
  FROM assignments AS a
  GROUP BY a.teacher_id
  ORDER BY AVG(a.assisgnment_id)
  LIMIT 1
) AS t ON a.teacher_id = t.teacher_id
GROUP BY s.full_name
ORDER BY AVG(ag.grade) DESC;
