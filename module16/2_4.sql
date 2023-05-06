SELECT customer.full_name, "order".order_no
FROM customer
JOIN "order" ON customer.customer_id = "order".customer_id
WHERE customer.manager_id IS NULL;
