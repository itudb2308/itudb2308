UPDATE FROM products 
WHERE id = {id}
SET cost = {cost}, category = {category}, name = {name}, brand = {brand}, retail_price = {retail_price}, department = {department}, sku = {sku}, distribution_center_id = {distribution_center_id}
RETURNING id;
