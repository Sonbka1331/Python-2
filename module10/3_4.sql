SELECT COUNT(DISTINCT t1.id) AS num_matching_rows
FROM table_1 t1
JOIN table_2 t2 ON t1.value = t2.value
JOIN table_3 t3 ON t1.value = t3.value;
