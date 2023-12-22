SELECT p.id, p.name, p.brand, p.category, count(*) as quantity, dc.id, dc.name, oi.sale_price
FROM order_items AS oi
         LEFT JOIN products p ON p.id = oi.product_id
         LEFT JOIN distribution_centers dc ON dc.id = p.distribution_center_id
WHERE oi.order_id = {orderId}
GROUP BY p.id, p.name, p.brand, p.category, dc.id, dc.name, oi.sale_price;
