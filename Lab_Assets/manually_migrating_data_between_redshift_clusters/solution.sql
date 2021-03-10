UNLOAD ('select * from users_data')
TO '<users-data-bucket>'
IAM_ROLE '<RedshiftS3 ARN>'
FORMAT AS PARQUET;

create table users_data(
    id_value varchar(64),
    name_first varchar(64),
    name_last varchar(64),
    location_country varchar(32),
    dob_age int,
    picture_large varchar(64),
    primary key(id_value)
) 
distkey(location_country) 
compound sortkey(id_value);

COPY users_data 
FROM '<users-data-bucket>' 
IAM_ROLE '<RedshiftS3 ARN>' 
FORMAT AS PARQUET;