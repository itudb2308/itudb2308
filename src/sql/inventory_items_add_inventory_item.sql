INSERT INTO inventory_items (product_id,created_at,cost,product_category,product_name,product_brand,product_retail_price,
                            product_department,product_sku,product_distribution_center_id)
VALUES ({product_id}, '{created_at}', {cost}, '{product_category}', '{product_name}', '{product_brand}', {product_retail_price},
        '{product_department}', '{product_sku}', {product_distribution_center_id})
RETURNING id;