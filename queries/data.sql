SELECT input.userID, inputTime, direction, team
FROM input
INNER JOIN teamAssign
ON input.userID = teamAssign.userID
WHERE inputTime > (now() - interval %s)
ORDER BY inputTime ASC;