/**********************************************************************************************************/
-- Proc: Basic data pipeline from Snowflake internal stage
-- CreateBy: Martin Palkovic
-- Create date: 2022-10-31
-- Description: Basic workflow for building the latter portions of a data pipeline within Snowflake.
-- Note that this code assumes you have loaded a csv file into a Snowflake internal stage via a 
-- 3rd party or open source integration tool
/***********************************************************************************************************/

/* initialize environment */
use role sysadmin;
use warehouse reporting_wh;
use database my_dev_database;
use schema my_schema;

/* Provides information for your third party/open source integration tool */
desc table dimcustomer;

/* create stage, if needed */
show stages;
-- create or replace my_stage 
list @my_stage;

/* create file format */
create or replace file format my_file_format
type = 'CSV'
field_delimiter = ','
replace_invalid_characters = TRUE
null_if = ('');

/* create stored procedure */
create or replace procedure dim_customer_pipeline()
returns varchar
language sql
execute as caller
as
$$
begin
    truncate table MY_SCHEMA.DIMCUSTOMER;

    copy into
        MY_SCHEMA.DIMCUSTOMER
        from
        ( select t1.$1
                ,t1.$2
                ,t1.$3
                ,nullif(t1.$4, '')
            from @MY_SCHEMA.MY_STAGE/Dim_Customer.csv.gz (file_format => 'my_file_format') t1 
    )
    file_format=my_file_format ON_ERROR='SKIP_FILE';

    remove @MY_SCHEMA.MY_STAGE pattern='.*Customer.*';

    return 'Successfully loaded data into MY_DEV_DATABASE.MY_SCHEMA.DIMCUSTOMER';
 end;
 $$
;

/* create task */
create or replace task dim_customer
    warehouse = LOAD_WH
    schedule = 'using cron 30 9 * * * UTC'
    comment = 'Truncates MY_DEV_DATABASE.MY_SCHEMA.DIMCUSTOMER, loads all rows of the dimcustomer table from Azure SQL and deletes the csv from the staging area'
    as
    call dim_customer_pipeline();

/* grant execute task priveleges to role sysadmin */
use role accountadmin;
grant execute task on account to role sysadmin;

/* tasks are created in a suspended state by default, you must 'resume' them to schedule them */
use role sysadmin;
alter task dim_customer resume;

/* confirm that the tasks are working */
 show tasks;
 select * from table(information_schema.task_history()) order by scheduled_time;