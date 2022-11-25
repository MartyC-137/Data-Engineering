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
    sql string;
    final_sql string;
    c1 cursor for (select COMPANY_NAME from DEV.MY_SCHEMA.MY_TABLE);
    my_results resultset;
begin
    final_sql := '';
    
    for record in c1 do
        sql := $$select 'COMPANY_NAME' as Company
            , GL.ACTNUM as Account_Number
            , G1.DESCRIPTION as Account_Name
            from GP.COMPANY_NAME.General_Ledger_Table GL 

            inner join GP.COMPANY_NAME.Account_Name_Table G1
                on G1.ID = GL.ID
            $$;
        sql := replace(sql, 'COMPANY_NAME', record.COMPANY_NAME);

        if(final_sql <> '')then 
          final_sql := final_sql || ' union all ';
        end if;

        final_sql := final_sql || sql;
    end for;
    
    my_results := (execute immediate :final_sql);
    return table(my_results);
end;