/**********************************************************************************************************/
-- Query: Flatten JSON to analytics view in Snowflake 
-- CreateBy: Martin Palkovic
-- Create date: 2021-05-03
-- Description: SQL code for creating a materialized view in Snowflake from a JSON in your staging area
-- Modified by:
-- Modify date:
-- Mod Reason:
/***********************************************************************************************************/

create or replace materialized view my_db.schema.my_view
as
select
    jsn.value:Id::string as ID
  , jsn.value:TotalAmount::number(10,2) as Total_Amount
  , jsn.value:Cash::boolean as Cash
  , jsn.value:TransactionDate::date as Transaction_Date
  from staging_area.schema.my_table
  , lateral flatten (input => JSON_DATA) as jsn

qualify row_number()
over (
  partition by jsn.value:Id
  order by jsn.value:Id) = 1;

/*
Input:
Row  JSON_DATA
1    [{"Id": 1,"TotalAmount": 42.75, "Cash": true,"TransactionDate": "2022-03-25T18:44:46.54"}]
2    [{"Id":2, "TotalAmount": 57.99, "Cash": false, "TransactionDate": "2022-03-28T12:24:33.12"}]
3    [{"Id": 1,"TotalAmount": 42.75, "Cash": true,"TransactionDate": "2022-03-25T18:44:46.54"}]
4    [{"Id": 3, "TotalAmount": 100.25, "Cash": false, "TransactionDate": "2022-04-01T06:10:15.30"}]

Output:
ID Total_Amount  Cash   Transaction_Date
1  42.75         True   2022-03-25
2  57.99         False  2022-03-28
3  100.25        False  2022-04-01
*/