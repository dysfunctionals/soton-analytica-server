CREATE TYPE direction AS ENUM ('left', 'none', 'right');
CREATE TYPE team AS ENUM ('zucc', 'user');

CREATE TABLE teamAssign (
    userID TEXT,
    team team,
    alive BOOLEAN
);

CREATE TABLE input (
    userID TEXT,
    direction direction,
    inputTime TIMESTAMP
);

CREATE INDEX ON teamAssign(userID);
CREATE INDEX ON input(userID);
CREATE INDEX ON input(inputTime);