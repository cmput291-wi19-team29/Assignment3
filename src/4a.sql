-- get the number of cessions that each author will be participating in
-- authors only participate if their paper is accepted
-- according to the forum, the session count is non distinct

SELECT author, COUNT(csession) as "Number of Sessions"
FROM papers
WHERE decision = "A"
GROUP BY author
