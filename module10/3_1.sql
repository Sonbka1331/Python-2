SELECT SUM(num_rows) AS total_rows FROM (
    SELECT COUNT(*) AS num_rows FROM table_1
    UNION ALL
    SELECT COUNT(*) AS num_rows FROM table_2
    UNION ALL
    SELECT COUNT(*) AS num_rows FROM table_3
);
