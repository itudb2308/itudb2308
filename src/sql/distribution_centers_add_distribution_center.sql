INSERT INTO distribution_centers (name,latitude,longitude) 
VALUES ('{name}', {latitude}, {longitude})
RETURNING id;