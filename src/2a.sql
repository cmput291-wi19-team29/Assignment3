--Show all papers* and allow one to be selected. 
--Once a papers is selected, show all potential reviewers for that paper. 
--Potential reviewers shown must have the same area of expertise as the paper. 
--If reviewer has already reviewed the paper, they should not be able to review it again 
--(either don’t show them as a potential reviewer or give proper error once they try to input a review)
--Note: Show all papers in pages with each displayed page having 5 papers. (N) Next (P) Previous

SELECT p.title, p.id, p.area, p.author
FROM papers p;