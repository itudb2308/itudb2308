UPDATE inventory_items
SET
  inventory_items.sold_at = {current_time}
WHERE
  inventory_items.id = {product_id}
LIMIT {quantity};
