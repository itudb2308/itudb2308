SELECT p.id, p.name, p.brand, p.category, p.department, p.retail_price, SUM(CASE WHEN i.product_id IS NOT NULL AND i.sold_at IS NULL THEN 1 ELSE 0 END) as available_stocks
FROM products p
LEFT JOIN inventory_items i ON p.id = i.product_id
WHERE p.id = {product_id} 
GROUP BY p.id;

