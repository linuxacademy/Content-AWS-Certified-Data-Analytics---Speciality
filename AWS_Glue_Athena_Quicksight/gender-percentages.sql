SELECT gender, (COUNT(gender) * 100.0 / (SELECT COUNT(*) FROM transformed_data)) AS percent
FROM transformed_data
GROUP BY gender;