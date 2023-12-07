UPDATE distribution_centers
SET name = '{name}', latitude = {latitude}, longitude = {longitude}
WHERE id = {id}
RETURNING id;