CREATE TABLE IF NOT EXISTs products
(
    id                            INTEGER PRIMARY KEY,
    cost                          FLOAT,
    category                      VARCHAR(50),    -- Max length 29
    name                          VARCHAR(250),   -- Max length 224
    brand                         VARCHAR(50),    -- Max length 41
    retail_price                  FLOAT,
    department                    VARCHAR(5),     -- Max length 5
    sku                           VARCHAR(50),    -- Max length 32
    distribution_center_id        INTEGER REFERENCES distribution_centers,
);