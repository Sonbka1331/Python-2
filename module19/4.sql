SELECT sg.group_id,
       AVG(COALESCE(
            (SELECT COUNT(*)
             FROM assignments AS a
             INNER JOIN assignments_grades AS ag ON a.assisgnment_id = ag.assisgnment_id
             WHERE s.student_id = ag.student_id AND a.due_date < ag.date
            ), 0)) AS avg_late_assignments,
       MAX(COALESCE(
            (SELECT COUNT(*)
             FROM assignments AS a
             INNER JOIN assignments_grades AS ag ON a.assisgnment_id = ag.assisgnment_id
             WHERE s.student_id = ag.student_id AND a.due_date < ag.date
            ), 0)) AS max_late_assignments,
       MIN(COALESCE(
            (SELECT COUNT(*)
             FROM assignments AS a
             INNER JOIN assignments_grades AS ag ON a.assisgnment_id = ag.assisgnment_id
             WHERE s.student_id = ag.student_id AND a.due_date < ag.date
            ), 0)) AS min_late_assignments
FROM students_groups AS sg
LEFT JOIN students AS s ON sg.group_id = s.group_id
GROUP BY sg.group_id;
