SELECT p.model, price
FROM Product p, PC pp
WHERE p.model=pp.model
AND maker='B'
UNION
SELECT p.model, price
FROM Product p, printer pp
WHERE p.model=pp.model
AND maker='B'
UNION
SELECT p.model, price
FROM Product p, laptop pp
WHERE p.model=pp.model
AND maker='B'

