-- Change ownership of all tables in a schema to a different role
-- My organization's data pipelines are often set up to use service accounts - 
-- these accounts can only insert data into Snowflake if a certain role owns the table.
use warehouse reporting_wh;
use database my_db;

grant ownership on schema my_db.schema to role STAGING_ADMIN;
grant ownership on all tables in schema my_db.schema to role STAGING_ADMIN copy current grants;
