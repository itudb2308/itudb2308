CREATE TABLE IF NOT EXISTS events
(
    id              INTEGER primary key,
    user_id         INTEGER references users,
    sequence_number INTEGER,
    session_id      CHAR(36),
    created_at      TIMESTAMP,
    ip_address      VARCHAR(20),
    city            VARCHAR(50),
    country         VARCHAR(40),
    postal_code     VARCHAR(15),
    browser         VARCHAR(10),
    traffic_source  VARCHAR(10),
    uri             VARCHAR(100),
    event_type      VARCHAR(15)
);