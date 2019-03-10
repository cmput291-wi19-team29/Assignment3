-- get reviewers that did not review any papers
-- reviewers are those users that have an expertise

SELECT e.reviewer 
  FROM expertise e 
 WHERE NOT EXISTS 
       (
         SELECT * 
           FROM reviews 
          WHERE reviews.reviewer == e.reviewer
       );