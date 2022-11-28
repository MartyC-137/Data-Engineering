/**********************************************************************/
-- Title: How to shorten a huge union query
-- By: Martin Palkovic
-- Date: 2022-11-25
-- Description: Have you encountered a production small_sql query with a large number of unions,
-- and very little changes between the queries except perhaps the database and/or schema name?
-- In this example, you can loop over the COMPANY_NAME field in MY_TABLE to create
-- one select statement per 'COMPANY_NAME', union them together, and return the results
-- in one go. The first implementation of this at work reduced a 300 line query to ~ 40 lines!
/*********************************************************************/

use role sysadmin;
use warehouse my_wh;
use database dev;

-- Declare variables, loop over results of the 'organization' cursor variable
declare
    small_sql varchar;
    big_sql varchar;
    organization cursor for (select COMPANY_NAME from MY_SCHEMA.MY_TABLE);
    my_results resultset;
begin
    big_sql := '';
    -- In Snowflake, $$ is a multi-line string delimiter 
    for company in organization do
        small_sql := $$select 'COMPANY_NAME' as Company
            , GL.ACTNUM as Account_Number
            , ACT.DESCRIPTION as Account_Name
            from COMPANY_NAME.General_Ledger_Table GL 

            inner join COMPANY_NAME.Account_Name_Table ACT
                on ACT.ID = GL.ID
            $$;
        small_sql := replace(small_sql, 'COMPANY_NAME', company.COMPANY_NAME);

        if(big_sql != '') then 
          big_sql := big_sql || ' union all ';
        end if;

        big_sql := big_sql || small_sql;
    end for;
    
    my_results := (execute immediate :big_sql);
    return table(my_results);
end;