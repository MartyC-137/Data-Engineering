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
USE WAREHOUSE REPORTING_WH;
USE DATABASE STAGING_DEV;
USE SCHEMA NS_LANDING;

CREATE OR REPLACE PROCEDURE sp_clean_stage( stage_name VARCHAR, DAYS number, DRY_RUN boolean )
RETURNS varchar
LANGUAGE sql
EXECUTE AS CALLER
AS
$$
DECLARE
    ListFiles RESULTSET;
    LastModified DATE;
    RemovedCount NUMBER := 0;
    TotalCount NUMBER := 0;
BEGIN
    ListFiles := (EXECUTE IMMEDIATE 'LS @' || stage_name );
    LET C1 CURSOR FOR ListFiles; 
    FOR files IN C1 DO
       TotalCount := TotalCount + 1;
       LastModified := TO_DATE(LEFT( files."last_modified", LENGTH(files."last_modified") - 4 ), 'DY, DD MON YYYY HH24:MI:SS' );
       IF (LastModified <= DATEADD( 'day', -1 * DAYS, current_timestamp())) THEN 
            RemovedCount := RemovedCount + 1;                
            IF (NOT DRY_RUN) THEN
                EXECUTE IMMEDIATE 'RM @' || files."name";
            END IF;
       END IF;
    END FOR;
    RETURN RemovedCount || ' of ' || TotalCount || ' files ' || IFF(DRY_RUN,'will be','were') || ' deleted.';
END;
$$;

-- Run Stored Procedure
-- USE DATABASE STAGING_PROD;
-- CALL sp_clean_stage('your_stage_here', 14, false);