/**********************************************************************/
-- Title: How to shorten a huge union query
-- By: Martin Palkovic
-- Date: 2022-11-25
-- Description: Have you encountered a production SQL query with a large number of unions,
-- and very little changes between the queries except perhaps the database and/or schema name?
-- In this example, you can loop over the COMPANY_NAME field in MY_TABLE to create
-- one select statement per 'COMPANY_NAME', union them together, and return the results
-- in one go. The first implementation of this at work reduced a 300 line query to ~ 40 lines!
/*********************************************************************/

declare
    sql varchar;
    final_sql varchar;
    organization cursor for (select COMPANY_NAME from DEV.MY_SCHEMA.MY_TABLE);
    my_results resultset;
begin
    final_sql := '';
    
    for company in organization do
        sql := $$select 'COMPANY_NAME' as Company
            , GL.ACTNUM as Account_Number
            , ACT.DESCRIPTION as Account_Name
            from GP.COMPANY_NAME.General_Ledger_Table GL 

            inner join GP.COMPANY_NAME.Account_Name_Table ACT
                on ACT.ID = GL.ID
            $$;
        sql := replace(sql, 'COMPANY_NAME', company.COMPANY_NAME);

        if(final_sql != '')then 
          final_sql := final_sql || ' union all ';
        end if;

        final_sql := final_sql || sql;
    end for;
    
    my_results := (execute immediate :final_sql);
    return table(my_results);
end;