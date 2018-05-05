SELECT i.userID
FROM (
    SELECT userID, max(inputTime) AS inputTime
    FROM input
    GROUP BY userID
) AS i
WHERE i.inputTime < (now() - interval '10 seconds');
