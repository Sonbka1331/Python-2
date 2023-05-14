SELECT COUNT(*) AS num_matching_rows
FROM table_1
WHERE value IN (SELECT value FROM table_2);
