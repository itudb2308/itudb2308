UPDATE products 
SET cost = {cost}, category = '{category}', name = '{name}', brand = '{brand}', retail_price = {retail_price}, department = '{department}', distribution_center_id = {distribution_center_id}
WHERE id = {id}
RETURNING id;