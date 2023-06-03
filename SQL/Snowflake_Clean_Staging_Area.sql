/*******************************************************************/
-- Procedure: sp_clean_stage
-- Created By: Martin Palkovic
-- Create date: 2022-08-16
-- Organization: Cooke Inc.
-- Summary: Delete files from a named Snowflake staging area
-- Description: In data pipelines, we sometimes stick files in a named 
-- Snowflake internal staging area - occasionally, you'll want to purge the 
-- files from here. Append this stored procedure call as the last step in your pipeline
-- to keep your staging area clean
/*******************************************************************/
use warehouse REPORTING_WH;
use database STAGING_DEV;
use schema NS_LANDING;

create or replace procedure sp_clean_stage(
    stage_name varchar, DAYS number, DRY_RUN boolean
)
returns varchar
language sql
execute as caller
as
$$
declare
    ListFiles resultset;
    LastModified date;
    RemovedCount number := 0;
    TotalCount number := 0;
begin
    ListFiles := (execute immediate 'ls @' || stage_name );
    let C1 cursor for ListFiles; 
    for files in C1 do
       TotalCount := TotalCount + 1;
       LastModified := to_date(left( files."last_modified", length(files."last_modified") - 4 ), 'DY, DD MON YYYY HH24:MI:SS' );
       if (LastModified <= dateadd( 'day', -1 * days, current_timestamp())) then 
            RemovedCount := RemovedCount + 1;                
            if (not dry_run) then
                execute immediate 'rm @' || files."name";
            end if;
       end if;
    end for;
    return RemovedCount || ' of ' || TotalCount || ' files ' || iff(dry_run,'will be','were') || ' deleted.';
end;
$$;

-- Run Stored Procedure
-- use database my_db;
-- call sp_clean_stage('my_stage', 14, false);
