SELECT *
FROM order_items AS oi
         LEFT JOIN products p ON p.id = oi.product_id
         LEFT JOIN distribution_centers dc ON dc.id = p.distribution_center_id
WHERE oi.order_id = {orderId};
