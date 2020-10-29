SELECT "dob.age", COUNT("dob.age") AS occurances 
FROM transformed_data
GROUP BY "dob.age"
ORDER BY occurances DESC
LIMIT 5;