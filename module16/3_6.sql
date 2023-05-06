SELECT maker, speed
FROM Product p, Laptop l
WHERE p.type = 'Laptop'
AND p.maker = l.maker
AND l.hd >= 10
