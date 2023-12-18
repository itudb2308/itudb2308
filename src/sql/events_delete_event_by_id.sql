DELETE FROM events 
WHERE id = {id}
RETURNING id;