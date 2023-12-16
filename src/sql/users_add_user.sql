INSERT INTO users (id, first_name, last_name, email, age, gender, state, street_address, postal_code, city, country, latitude, longitude, traffic_source, created_at)
VALUES(DEFAULT, '{first_name}', '{last_name}','{email}', {age}, '{gender}', '{state}', '{street_address}', '{postal_code}', '{city}', '{country}', {latitude}, {longitude}, '{traffic_source}', '{created_at}')
RETURNING id;