SELECT distinct battle
FROM Classes
inner JOIN Ships  ON ships.class = classes.class
inner JOIN Outcomes  ON Classes.class=Outcomes.ship or Ships.name=Outcomes.ship
WHERE classes.class = 'Kongo'
