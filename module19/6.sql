SELECT AVG(grade) AS avg_grade
FROM assignments_grades
WHERE assisgnment_id IN (
  SELECT assisgnment_id
  FROM assignments
  WHERE assignments.assignment_text LIKE '%прочитать%' OR assignments.assignment_text LIKE '%запомнить%'
);
