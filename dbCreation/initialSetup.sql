CREATE TYPE direction AS ENUM ('left', 'none', 'right');
CREATE TYPE team AS ENUM ('zucc', 'user');

CREATE TABLE teamAssign (
    userID TEXT,
    team team
);

CREATE TABLE input (
    userID TEXT,
    direction direction,
    inputTime TEXT
);