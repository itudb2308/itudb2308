INSERT INTO products (cost, category, name, brand, retail_price, department, sku, distribution_center_id)
VALUES({cost}, '{category}', '{name}','{brand}', {retail_price}, '{department}', '{sku}', {distribution_center_id})
RETURNING id;