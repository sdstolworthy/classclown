-- SQLite
SELECT title, price, url, description, created_at from classifieds_airplane where title like '%piper%' or description like '%piper%' order by strftime('%m%d', created_at) desc, price asc;