update orders
set status = '{order_status}'
{update_timestamp} ,{timestamp_column_name} = now()
where id = {order_id};
update order_items
set status = '{order_status}'
{update_timestamp} ,{timestamp_column_name} = now()
where order_id = {order_id};
