SELECT sg.group_id, AVG(COALESCE(total_late_assignments, 0)) AS avg_late_assignments,
       MAX(COALESCE(total_late_assignments, 0)) AS max_late_assignments,
       MIN(COALESCE(total_late_assignments, 0)) AS min_late_assignments
FROM students_groups AS sg
LEFT JOIN students AS s ON sg.group_id = s.group_id
LEFT JOIN (
    SELECT ag.student_id, COUNT(*) AS total_late_assignments
    FROM assignments AS a
    INNER JOIN assignments_grades AS ag ON a.assisgnment_id = ag.assisgnment_id
    WHERE a.due_date < ag.date
    GROUP BY ag.student_id
) AS tla ON s.student_id = tla.student_id
GROUP BY sg.group_id
