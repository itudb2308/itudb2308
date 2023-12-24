DROP TABLE IF EXISTS  products, inventory_items, orders, order_items, users, events, distribution_centers;

--DELIMETER-FOR-PARSER--

CREATE TABLE IF NOT EXISTS distribution_centers
(
    id        BIGSERIAL PRIMARY KEY,
    name      VARCHAR(50),
    latitude  DOUBLE PRECISION,
    longitude DOUBLE PRECISION
);

--DELIMETER-FOR-PARSER--

CREATE TABLE IF NOT EXISTS users
(
    id             BIGSERIAL PRIMARY KEY,
    first_name     VARCHAR(20),
    last_name      VARCHAR(20),
    email          VARCHAR(100) UNIQUE,
    age            BIGINT,
    gender         CHAR(1),
    state          VARCHAR(20),
    street_address VARCHAR(150),
    postal_code    VARCHAR(15),
    city           VARCHAR(20),
    country        VARCHAR(20),
    latitude       DOUBLE PRECISION,
    longitude      DOUBLE PRECISION,
    traffic_source VARCHAR(20),
    created_at     TIMESTAMP
);

--DELIMETER-FOR-PARSER--

CREATE TABLE IF NOT EXISTS events
(
    id              BIGSERIAL PRIMARY KEY,
    user_id         BIGINT REFERENCES users(id) ON DELETE CASCADE ON UPDATE CASCADE,
    sequence_number BIGINT,
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

--DELIMETER-FOR-PARSER--

CREATE TABLE IF NOT EXISTS products
(
    id                     BIGSERIAL PRIMARY KEY,
    cost                   DOUBLE PRECISION,
    category               VARCHAR(50),
    name                   VARCHAR(250),
    brand                  VARCHAR(50),
    retail_price           DOUBLE PRECISION,
    department             VARCHAR(5),
    sku                    CHAR(32),
    distribution_center_id BIGINT REFERENCES distribution_centers(id) ON DELETE CASCADE ON UPDATE CASCADE
);

--DELIMETER-FOR-PARSER--

CREATE TABLE IF NOT EXISTS inventory_items
(
    id                             BIGSERIAL PRIMARY KEY,
    product_id                     BIGINT REFERENCES products(id) ON DELETE CASCADE ON UPDATE CASCADE,
    created_at                     TIMESTAMP,
    sold_at                        TIMESTAMP,
    cost                           DOUBLE PRECISION,
    product_category               VARCHAR(50),
    product_name                   VARCHAR(250),
    product_brand                  VARCHAR(50),
    product_retail_price           DOUBLE PRECISION,
    product_department             VARCHAR(5),
    product_sku                    VARCHAR(50),
    product_distribution_center_id BIGINT REFERENCES distribution_centers(id) ON DELETE CASCADE ON UPDATE CASCADE
);

--DELIMETER-FOR-PARSER--

CREATE TABLE IF NOT EXISTS orders
(
    id           BIGSERIAL PRIMARY KEY,
    user_id      BIGINT REFERENCES users(id) ON DELETE CASCADE ON UPDATE CASCADE,
    status       VARCHAR(10),
    gender       CHAR(1),
    created_at   TIMESTAMP,
    returned_at  TIMESTAMP,
    shipped_at   TIMESTAMP,
    delivered_at TIMESTAMP,
    num_of_item  BIGINT
);

--DELIMETER-FOR-PARSER--

CREATE TABLE IF NOT EXISTS order_items
(
    id                BIGSERIAL PRIMARY KEY,
    order_id          BIGINT REFERENCES orders(id) ON DELETE CASCADE ON UPDATE CASCADE,
    user_id           BIGINT REFERENCES users(id) ON DELETE CASCADE ON UPDATE CASCADE,
    product_id        BIGINT REFERENCES products(id) ON DELETE CASCADE ON UPDATE CASCADE,
    inventory_item_id BIGINT REFERENCES inventory_items(id) ON DELETE CASCADE ON UPDATE CASCADE,
    status            VARCHAR(10),
    created_at        TIMESTAMP,
    shipped_at        TIMESTAMP,
    delivered_at      TIMESTAMP,
    returned_at       TIMESTAMP,
    sale_price        DOUBLE PRECISION
);

--DELIMETER-FOR-PARSER--

CREATE OR REPLACE FUNCTION update_inventory_item()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE inventory_items
    SET cost = NEW.cost,
        product_category = NEW.category,
        product_name = NEW.name,
        product_brand = NEW.brand,
        product_retail_price = NEW.retail_price,
        product_department = NEW.department,
        product_sku = NEW.sku,
        product_distribution_center_id = NEW.distribution_center_id
    WHERE product_id = NEW.id;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

--DELIMETER-FOR-PARSER--

CREATE TRIGGER update_product_trigger
AFTER UPDATE ON products
FOR EACH ROW
EXECUTE FUNCTION update_inventory_item();