-- First get all potential reviewers with a matching area of expertise
SELECT e.reviewer 
FROM expertise e, papers p 
WHERE p.area = e.area 
AND p.id = ?
EXCEPT -- now subtract people who have already reviewed this paper
SELECT r.reviewer 
FROM expertise e, papers p, reviews r
WHERE r.paper = p.id 
AND e.reviewer=r.reviewer
AND e.area=p.area -- don't want to catch reviews by people in different areas
AND p.id = ?;

-- NOTE: This can return the paper's author,
-- but the assignment spec doesn't say anything about that, so I'm leaving it.