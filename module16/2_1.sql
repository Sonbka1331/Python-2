SELECT customer.full_name, manager.full_name, "order".purchase_amount, "order".date
FROM "order"
JOIN customer ON "order".customer_id = customer.customer_id
JOIN manager ON "order".manager_id = manager.manager_id
