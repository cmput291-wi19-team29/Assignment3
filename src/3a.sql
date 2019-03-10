-- given a number range, find all reviewers whose number of reviews is in that range (the range should include the bounds)
-- args are in the format [a, b]

  SELECT reviewer 
    FROM reviews 
GROUP BY reviewer 
  HAVING COUNT(*) >= ? 
     AND COUNT(*) <= ?;