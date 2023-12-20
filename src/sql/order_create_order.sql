insert into orders (user_id, status, gender, created_at, num_of_item)
values ({user_id}, 'Processing', '{user_gender}', now(), {num_of_item})
returning id;
