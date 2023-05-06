SELECT distinct c.class
FROM
(
SELECT s.class, s.name
FROM Ships s
UNION
SELECT o.ship as 'class', o.ship
FROM Outcomes o
WHERE NOT EXISTS( SELECT * FROM Ships s WHERE s.name = o.ship)
) s
INNER JOIN Classes c ON (c.class = s.class) AND (c.class = s.name)
