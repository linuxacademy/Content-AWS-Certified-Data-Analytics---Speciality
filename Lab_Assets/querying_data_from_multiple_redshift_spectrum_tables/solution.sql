create external schema users_data
from data catalog   
database 'users'
iam_role ''
create external database if not exists;


create external table users_data.names(
  id_name varchar(32),
  id_value varchar(64),
  gender varchar(16),
  name_title varchar(32),
  name_first varchar(64),
  name_last varchar(64)
)
ROW FORMAT SERDE
    'org.openx.data.jsonserde.JsonSerDe'
LOCATION '';

create external table users_data.location(
    id_name varchar(32),
    id_value varchar(32),
    location_street_number int,
    location_street_name varchar(64),
    location_city varchar(32),
    location_state varchar(32),
    location_country varchar(32),
    location_postcode varchar(32),
    location_coordinates_latitude varchar(64),
    location_coordinates_longitude varchar(64),
    location_timezone_offset varchar(32),
    location_timezone_description varchar(32),
    nat varchar(16)
)
ROW FORMAT SERDE
    'org.openx.data.jsonserde.JsonSerDe'
LOCATION '';

create external table users_data.age(
    id_name varchar(32),
    id_value varchar(32),
    dob_date varchar(32),
    dob_age int,
    registered_date varchar(32),
    registered_age int
)
ROW FORMAT SERDE
    'org.openx.data.jsonserde.JsonSerDe'
LOCATION '';

create external table users_data.contact(
    id_name varchar(32),
    id_value varchar(32),
    email varchar(32),
    phone varchar(32),
    cell varchar(32)
)
ROW FORMAT SERDE
    'org.openx.data.jsonserde.JsonSerDe'
LOCATION '';

create external table users_data.picture(
    id_name varchar(32),
    id_value varchar(32),
    picture_large varchar(64),
    picture_medium varchar(64),
    picture_thumbnail varchar(64)
)
ROW FORMAT SERDE
    'org.openx.data.jsonserde.JsonSerDe'
LOCATION '';

select 
    names.name_first as first_name, 
    names.name_last as last_name, 
    location.location_state as state, 
    age.dob_age as age, 
    contact.cell as cell, 
    picture.picture_large as picture
from users_data.names
    join users_data.location on users_data.names.id_value = users_data.location.id_value 
    join users_data.age on users_data.names.id_value = users_data.age.id_value 
    join users_data.contact on users_data.names.id_value = users_data.contact.id_value
    join users_data.picture on users_data.names.id_value = users_data.picture.id_value
order by age
limit 10;