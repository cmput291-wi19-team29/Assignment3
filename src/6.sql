-- for each reviewer, give a bar chart of their average review scores for each category. You must return a single grouped bar chart.

  SELECT reviewer, 
         AVG(originality) AS "Average Originality", 
         AVG(importance) AS "Average Importance", 
         AVG(soundness) AS "Average Soundness", 
         AVG(overall) AS "Average Overall" 
    FROM reviews 
GROUP BY reviewer;