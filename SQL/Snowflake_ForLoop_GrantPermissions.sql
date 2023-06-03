/* ######################### */
/* Script: Revoke/Grant permissions for reader accounts in Snowflake  */
/* Author: Martin Palkovic  */
/* Date: 2023-02-09  */
/* Description: This script loops through query results from the information_schema and grants privileges only to tables */
/* that have > 0 rows. This script was inspired by a database containing ~2,500 tables, 400 of which contained >= 1 row of data. */
/* This script revokes all privileges and then grants select on tables with > 0 rows. Modify your cursor queries as needed to provide a */
/* list of tables, schemas etc. to loop over. */

-- Set session variables
set db = 'my_db';
set rl = 'accountadmin';
set wh = 'my_wh';
set role_var = '"My_Role"'; --the double quotes are required as this is a case sensitive string value!
set share_name = 'ab12345.my_secure_share';

-- Schemas to exclude. Set as desired, add as many as you need
set exc1 = 'information_schema';
set exc2 = 'my_schema1';

use database identifier($db);
use role identifier($rl);
use warehouse identifier($wh);

/* SHARE LEVEL - EXECUTED IN MAIN ACCOUNT */
-- Revoke privileges
declare 
    iter_schema cursor for (select * from information_schema.schemata where schema_name not in ($exc1, $exc2));
begin
    for s in iter_schema do
        execute immediate 'revoke select on all tables in schema ' || s.schema_name || ' from share identifier($share_name)';
    end for;
    return 'Permissions successfully revoked from secure share!';
end;

-- Add to share all tables that have > 0 rows
declare 
    iter_tables cursor for (select * from information_schema.tables 
                            where row_count > 0 and table_schema not in ($exc1, $exc2));
begin
    for t in iter_tables do
        execute immediate 'grant select on table ' || t.table_schema || '.' || t.table_name || ' to share identifier($share_name)';
    end for;
    return 'Permissions successfully granted to secure share!';
end;

/* SHARE LEVEL - EXECUTED IN READER ACCOUNT BY ADMIN */
-- Revoke privileges 
declare 
    iter_schema cursor for (select * from information_schema.schemata where schema_name not in ($exc1, $exc2));
begin
    for s in iter_schema do
        execute immediate 'revoke select on all tables in schema ' || s.schema_name || ' from role identifier($role_var)';
    end for;
    return 'Permissions successfully revoked!';
end;

-- Grant only permissions on tables that have > 0 rows
declare 
    iter_tables cursor for (select * from information_schema.tables 
                            where row_count > 0 and table_schema not in ($exc1, $exc2));
begin
    for t in iter_tables do
        execute immediate 'grant select on table ' || t.table_schema || '.' || t.table_name || ' to role identifier($role_var)';
    end for;
    return 'Permissions successfully granted!';
end;
