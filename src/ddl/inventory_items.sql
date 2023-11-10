CREATE TABLE IF NOT EXISTS inventory_items
(
    id                              INTEGER PRIMARY KEY,
    product_id                      INTEGER REFERENCES products,
    created_at                      TIMESTAMP,
    sold_at                         TIMESTAMP,
    cost                            FLOAT,
    product_category                VARCHAR(50),  -- Max length 29
    product_name                    VARCHAR(250), -- Max length 232
    product_brand                   VARCHAR(50),  -- Max length 41
    product_retail_price            FLOAT,
    product_department              VARCHAR(5),   -- Max length 5  
    product_sku                     VARCHAR(50),  -- Max length 32
    product_distribution_center_id  INTEGER
);