SELECT s.full_name AS student_name, AVG(ag.grade) AS average_grade
FROM students AS s
INNER JOIN assignments_grades AS ag ON s.student_id = ag.student_id
WHERE ag.assisgnment_id IN (
  SELECT a.assisgnment_id
  FROM assignments AS a
  WHERE a.teacher_id = (
    SELECT t.teacher_id
    FROM teachers AS t
    INNER JOIN assignments AS a ON t.teacher_id = a.teacher_id
    GROUP BY t.teacher_id
    ORDER BY AVG(a.assisgnment_id)
    LIMIT 1
  )
)
GROUP BY s.full_name
ORDER BY AVG(ag.grade) DESC;
