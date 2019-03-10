-- get the number of cessions that each author will be participating in
-- authors only participate if their paper is accepted
-- according to the forum, the session count is non distinct
-- this solution includes authors with 0 acceted papers

SELECT  p1.author, COUNT(csession) 
FROM (SELECT DISTINCT author FROM papers) as p1
LEFT JOIN papers ON (papers.author = p1.author AND papers.decision = "A"  ) 
GROUP BY p1.author
