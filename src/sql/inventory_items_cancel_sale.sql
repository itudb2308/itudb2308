UPDATE inventory_items
SET sold_at = Null
WHERE id = {inventory_item_id}
RETURNING *;