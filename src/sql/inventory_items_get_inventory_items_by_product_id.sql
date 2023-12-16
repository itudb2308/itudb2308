SELECT p.id, p.name, p.brand, p.category, p.department, p.retail_price, COUNT(*) as available_stocks
FROM products p
JOIN inventory_items i ON p.id = i.product_id
WHERE p.id = {product_id} AND i.sold_at IS NULL
GROUP BY p.id;