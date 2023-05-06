SELECT
    order.order_no,
    customer.full_name AS customer_name,
    manager.full_name AS manager_name
FROM
    order
    INNER JOIN customer ON order.customer_id = customer.customer_id
    INNER JOIN manager ON order.manager_id = manager.manager_id
WHERE
    customer.city != manager.city;
