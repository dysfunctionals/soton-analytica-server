SELECT count(*)
FROM (
    SELECT *
    FROM input
    INNER JOIN teamAssign
    WHERE input.userID = teamAssign.userID
)