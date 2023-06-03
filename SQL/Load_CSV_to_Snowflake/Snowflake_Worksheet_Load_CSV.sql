/*****************************************************/
-- Worksheet: Loading a local csv to a Snowflake table
-- Date: 2022-12-08
/*****************************************************/

/* Set session variables
Enter the relevant database, schema, table and file format names here
*/
set role_name = 'sysadmin';
set wh = 'reporting_wh';
set db = 'my_new_db';
set sch = 'my_schema';
set table_name = 'my_table';
set fileformat = 'my_file_format';
set stage_name = 'my_stage';

/* initialize session */
-- role, warehouse
use role identifier($role_name);
use warehouse identifier($wh);

-- database
create database if not exists identifier($db);
use database identifier($db);

-- schema
create schema if not exists identifier($sch);
use schema identifier($sch);

-- file format
create file format if not exists identifier($fileformat)
type = csv
field_delimiter = ','
empty_field_as_null = true
skip_header = 1
comment = 'file format for loading csv files to Snowflake';

-- stage
create stage if not exists identifier($stage_name)
    file_format = $fileformat; --this may need to be typed out
show stages;

-- table;
create table if not exists identifier($table_name) (
    field1 varchar,
    field2 number
);

/* the PUT command must be executed in the SnowSQL CLI!
See the following documentation on this topic:
https://docs.snowflake.com/en/user-guide/snowsql-install-config.html
https://docs.snowflake.com/en/user-guide/data-load-internal-tutorial.html

download link: https://developers.snowflake.com/snowsql/
put file://c:\your\filepath\here\my_file.csv;
*/

/* confirm that the PUT command worked */
list @my_stage;

copy into identifier($table_name)
from @my_stage/my_file.csv.gz --variables dont work in conjunction with the @ argument
file_format = (format_name = $fileformat)
on_error = 'skip_file';

-- confirm the COPY INTO command worked
select * from identifier($table_name);
