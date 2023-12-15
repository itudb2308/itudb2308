SELECT *, COUNT(*) OVER() as total_count
FROM products AS P
{where}
{order_by}
LIMIT {limit} OFFSET {offset};
