/************************************************************************/
-- Script: Simple Python stored procedure in Snowflake
-- Date: 2022-12-28
-- Description: One thing I frequently do is compare one field to another,
-- to determine if something exists in one dataset but not another. Does one table
-- contain sales orders, pallet numbers, or report ID's that the other table 
-- does not?

-- This stored procedure allows you to quickly determine that from within
-- the Snowflake environment
/************************************************************************/

use role sysadmin;
use warehouse reporting_wh;
use database dev;
use schema my_schema;

create or replace table mytable (amount number comment 'fake amounts for testing', fruits string comment 'fake types of fruit for testing');
create or replace table mytable2 like mytable;

insert into mytable values (1, 'apple'), (2, 'orange'), (5, 'grape'), (7, 'cantelope'), (9, 'pineapple'), (17, 'banana'), (21, 'tangerine');
insert into mytable2 values (1, 'apple'), (3, 'orange'), (5, 'grape'), (7, 'strawberry'), (10, 'pineapple'), (17, 'banana'), (22, 'raspberry');

-- select * from mytable;
-- select * from mytable2;

create or replace procedure print_differences(TABLE1 string, TABLE2 string, FIELD1 string, FIELD2 string)
returns array
language python 
runtime_version = '3.8'
packages = ('snowflake-snowpark-python', 'pandas')
handler = 'print_differences'
as 
$$
import pandas as pd

def print_differences(session, table1: str,table2: str,field1: str,field2: str):

    #read the tables into a snowpark dataframe
    table1 = session.table(table1)
    table2 = session.table(table2)

    #convert to pandas
    df1 = table1.to_pandas()
    df2 = table2.to_pandas()

    # convert the the fields of interest from each table to a list
    list1 = df1[field1].to_list()
    list2 = df2[field2].to_list()

    return [item for item in list1 if item not in list2]
$$;

call print_differences('MYTABLE2', 'MYTABLE', 'FRUITS', 'FRUITS');

-- output:
-- ["cantelope","tangerine"]
