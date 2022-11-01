/******************************************************************************/
-- Script: Basic CDC Pipeline using Streams and Tasks in Snowflake 
-- CreateBy: Martin Palkovic
-- Create date: 2022-11-01
-- Description: Basic implementation of a Streams/Tasks workflow in Snowflake.
-- Streams detect DML changes to one table and will update another table based
-- on those changes
/******************************************************************************/

/* Set session variables */
set db = 'my_db';
set schema_name = 'my_schema';
set table_name = 'my_table';
set stream_name = 'my_stream';

/* Initialize Environment */
use role sysadmin;
use warehouse reporting_wh;

create or replace database identifier($db);
create or replace schema identifier($schema_name);

use database identifier($db);
use schema identifier($schema_name);

create or replace table my_db.my_schema.my_table 
comment='My JSON data from API, streaming from the STAGING_PROD database'
clone STAGING_PROD.URNERBARRY.URNERBARRY_ITEMS;

create or replace stream identifier($stream_name) on table STAGING_PROD.my_schema.my_table;

/* quick diagnostic check */
show streams;
select * from my_stream;

create or replace procedure my_procedure()
returns varchar
language sql
execute as owner
as
$$
begin
merge into my_table DEST using (
    select * from my_stream
      qualify row_number() over (
      partition by json_data:ID order by insert_date) = 1
      ) SOURCE
        on DEST.json_data:ID = SOURCE.json_data:ID
when matched and metadata$action = 'INSERT' then 
update set DEST.json_data = SOURCE.json_data,
            DEST.insert_date = current_timestamp()
when not matched and metadata$action = 'INSERT' then 
insert (DEST.json_data, DEST.insert_date)
        values(SOURCE.json_data, current_timestamp());
return 'CDC records successfully inserted';
end;
$$;

create or replace task push_my_table
warehouse = LOAD_WH
schedule = 'using cron 15 11 * * * UTC' --8:15am AT
comment = 'Change data capture task that pulls over new UrnerBarry data once a day at 8:15am'
when system$stream_has_data('my_stream')
as
call my_procedure();

/* grant execute task priveleges to role sysadmin */
use role accountadmin;
grant execute task on account to role sysadmin;

/* tasks are created in a suspended state by default, you must 'resume' them to schedule them */
use role sysadmin;
alter task push_my_table resume;

select * from my_db.my_schema.my_table;

show tasks;
select * from table(information_schema.task_history()) order by scheduled_time;
