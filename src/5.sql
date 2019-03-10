SELECT area, count(area) AS count 
FROM papers 
GROUP BY area 
ORDER BY count DESC;