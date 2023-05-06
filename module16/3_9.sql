SELECT DISTINCT maker
FROM Product p, PC pp
WHERE p.model=pp.model
AND speed >= 450
