SELECT o.*, concat(u.first_name, ' ', u.last_name) as customer_name, COUNT(*) OVER() as total_count
FROM orders AS o
JOIN users u ON u.id = o.user_id
{where}
{order_by}
LIMIT {limit} OFFSET {offset};
