SELECT phone_color, MAX(sold_count) AS max_sold_count
FROM table_checkout
WHERE phone_color IN ('Red', 'Blue')
GROUP BY phone_color
HAVING max_sold_count = (
    SELECT MAX(sold_count) AS max_sold_count
    FROM table_checkout
    WHERE phone_color IN ('Red', 'Blue')
)
