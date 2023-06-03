/******************************************************************************/
-- Script: Basic CDC Pipeline using Streams and Tasks in Snowflake 
-- CreateBy: Martin Palkovic
-- Create date: 2022-11-01
-- Description: Basic implementation of a Streams/Tasks workflow in Snowflake.
-- Streams detect DML changes to one table and will update another table based
-- on those changes
/******************************************************************************/

/* Set session variables */
set role_name = 'sysadmin';
set wh = 'my_wh';
set db = 'my_db';
set schema_name = 'my_schema';
set dest_table = 'my_table';
set stream_name = 'my_stream';
set source_table = 'staging_db.staging_schema.staging_table';
set proc_name = 'my_procedure';
set task_name = 'push_my_table';

/* Initialize Environment */
use role identifier($role_name);
use warehouse identifier($wh);

create database if not exists identifier($db);
create schema if not exists identifier($schema_name);

use database identifier($db);
use schema identifier($schema_name);

create table if not exists identifier($dest_table)
comment = 'JSON data from API, streaming from the staging database'
clone identifier($source_table);

create stream if not exists identifier($stream_name) on table identifier($source_table)
comment = 'CDC stream from staging table to prod table';

/* quick diagnostic check */
show streams;
select * from identifier($stream_name);

create or replace procedure identifier($proc_name)()
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

create or replace task identifier($task_name)
    warehouse = LOAD_WH
    schedule = '1 minute'
    comment = 'Change data capture task that pulls over new data once a minute'
when system$stream_has_data ('my_stream')
as
    call my_procedure();

/* grant execute task priveleges to role sysadmin */
set role_name = 'accountadmin';
use role identifier($role_name);
grant execute task on account to role identifier($role_name);

/* tasks are created in a suspended state by default, you must 'resume' them to schedule them */
set role_name = 'sysadmin';
use role identifier($role_name);
alter task identifier($task_name) resume;

select * from identifier($my_table);

show tasks;
select * from table(information_schema.task_history()) order by scheduled_time;
