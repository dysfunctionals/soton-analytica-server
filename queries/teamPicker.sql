SELECT (zucc.count < human.count) AS teamIsZucc
FROM (
    SELECT 'all' AS all, count(*) AS count
    FROM teamAssign
    WHERE team = 'zucc'
) AS zucc
INNER JOIN (
    SELECT 'all' AS all, count(*) AS count
    FROM teamAssign
    WHERE team = 'user'
) AS human
ON zucc.all = human.all;