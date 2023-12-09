SELECT *, COUNT(*) OVER() as total_count
FROM users as u
{where}
{order_by}
LIMIT {limit} OFFSET {offset};