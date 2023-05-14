SELECT phone_color, SUM(sold_count) AS total_sold
FROM table_checkout
GROUP BY phone_color
ORDER BY total_sold DESC
LIMIT 5;
