CREATE TABLE IF NOT EXISTS users
(
    id             INTEGER PRIMARY KEY,
    first_name     VARCHAR(20),
    last_name      VARCHAR(20),
    email          VARCHAR(100),
    age            INTEGER,
    gender         CHAR(1),
    state          VARCHAR(20),
    street_address VARCHAR(150),
    postal_code    VARCHAR(15),
    city           VARCHAR(20),
    country        VARCHAR(20),
    latitude       FLOAT,
    longitude      FLOAT,
    traffic_source VARCHAR(20),
    created_at     TIMESTAMP
);
