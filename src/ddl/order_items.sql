CREATE TABLE IF NOT EXISTS order_items
(
    id                INTEGER PRIMARY KEY,
    order_id          INTEGER REFERENCES orders,
    user_id           INTEGER REFERENCES users,
    product_id        INTEGER REFERENCES products,
    inventory_item_id INTEGER REFERENCES inventory_items,
    status            VARCHAR(10),
    created_at        TIMESTAMP,
    shipped_at        TIMESTAMP,
    delivered_at      TIMESTAMP,
    returned_at       TIMESTAMP,
    sale_price        FLOAT
);
