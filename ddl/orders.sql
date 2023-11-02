CREATE TABLE IF NOT EXISTS orders
(
    id           INTEGER PRIMARY KEY,
    user_id      INTEGER REFERENCES users,
    status       VARCHAR(10),
    gender       CHAR(1),
    created_at   TIMESTAMP,
    returned_at  TIMESTAMP,
    shipped_at   TIMESTAMP,
    delivered_at TIMESTAMP,
    num_of_item  INTEGER
);
