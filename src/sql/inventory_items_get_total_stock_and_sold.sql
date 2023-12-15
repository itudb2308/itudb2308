SELECT
    SUM(CASE WHEN sold_at IS NULL THEN 1 ELSE 0 END) AS  total_stock ,
    SUM(CASE WHEN sold_at IS NOT NULL THEN 1 ELSE 0 END) AS total_sold
FROM inventory_items
WHERE inventory_items.product_id = {product_id}
    AND inventory_items.product_distribution_center_id = {distribution_center_id}