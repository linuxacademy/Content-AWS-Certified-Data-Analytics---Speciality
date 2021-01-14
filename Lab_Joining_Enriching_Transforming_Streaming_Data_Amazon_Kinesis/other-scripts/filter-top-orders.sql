CREATE OR REPLACE STREAM "DESTINATION_USER_DATA" (
    order_id VARCHAR(64), 
    user_id VARCHAR(16), 
    email VARCHAR(16), 
    first_name VARCHAR(16),
    last_name VARCHAR(16), 
    total_cost FLOAT
);
CREATE OR REPLACE PUMP "STREAM_PUMP" AS INSERT INTO "DESTINATION_USER_DATA"

SELECT STREAM "order_id", "user_id", "email", "first_name", "last_name", "total_cost"
FROM "SOURCE_SQL_STREAM_001"
WHERE "total_cost" >= 100;