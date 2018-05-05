SELECT input.userID, inputTime, direction, team
FROM input
INNER JOIN teamAssign
ON input.userID = teamAssign.userID
WHERE inputTime > (now() - interval '10 seconds')
ORDER BY inputTime ASC;