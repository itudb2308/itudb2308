DELETE FROM distribution_centers
WHERE id = {id}
RETURNING id;