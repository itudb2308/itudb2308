UPDATE inventory_items AS II_1
SET sold_at = now()
WHERE II_1.id in (SELECT II_2.id
                  FROM inventory_items AS II_2
                  WHERE II_2.product_id = {product_id}
                    AND II_2.sold_at is null
                  LIMIT {quantity})
RETURNING II_1.id, II_1.product_retail_price;
