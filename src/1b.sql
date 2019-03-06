-- find all the reviewers of a given paper

SELECT reviewer
FROM papers p, reviews r
WHERE p.id = r.paper
AND p.id = ?;
