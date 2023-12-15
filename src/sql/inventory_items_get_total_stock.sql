SELECT COUNT(*) 
FROM inventory_items 
WHERE inventory_items.product_id = {product_id} and inventory_items.sold_at IS NULL 
and inventory_items.product_distribution_center_id = {distribution_center_id}
