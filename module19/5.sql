SELECT
  g.group_id,
  COUNT(DISTINCT s.student_id) AS total_students,
  AVG(ag.grade) AS average_grade,
  COUNT(CASE WHEN ag.grade IS NULL THEN 1 END) AS unsubmitted_assignments,
  COUNT(CASE WHEN ag.date > a.due_date THEN 1 END) AS overdue_assignments,
  COUNT(CASE WHEN ag.grade < 50 THEN 1 END) AS failed_attempts,
  COUNT(CASE WHEN ag.grade >= 50 THEN 1 END) AS successful_attempts
FROM students_groups g
JOIN students s ON g.group_id = s.group_id
LEFT JOIN assignments a ON g.group_id = a.group_id
LEFT JOIN assignments_grades ag ON a.assisgnment_id = ag.assisgnment_id AND s.student_id = ag.student_id
GROUP BY g.group_id;
