DELETE FROM products 
WHERE id = {id}
RETURNING id;
