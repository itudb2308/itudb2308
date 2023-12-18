UPDATE users 
SET first_name = '{first_name}', last_name = '{last_name}', email = '{email}', age = {age}, gender = '{gender}', country = '{country}', city = '{city}', state = '{state}', street_address = '{street_address}', postal_code = '{postal_code}'
WHERE id = {id}
RETURNING id;