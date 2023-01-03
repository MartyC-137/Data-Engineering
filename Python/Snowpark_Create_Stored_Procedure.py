# This only runs on a Python 3.8 environment

#import modules
import os, snowflake
import pandas as pd

from snowflake.snowpark import Session
from snowflake.snowpark.types import StringType

from dotenv import load_dotenv
load_dotenv()

# Establish Snowflake Connection
account = os.getenv('SNOWFLAKE_ACCT')
user = os.getenv('SNOWFLAKE_USER')
password = os.getenv('SNOWFLAKE_PASSWORD')
role = os.getenv('SNOWFLAKE_ROLE')
warehouse = 'REPORTING_WH'
database = 'STAGING_DEV'
schema = 'MISC'

def snowpark_cnxn(account, user, password, role, warehouse, database, schema):
    connection_parameters = {
        "account": account,
        "user": user,
        "password": password,
        "role": role,
        "warehouse": warehouse,
        "database": database,
        "schema": schema
    }
    session = Session.builder.configs(connection_parameters).create()
    return session

print('Connecting to Snowpark...\n')
session = snowpark_cnxn(account, user, password, role, warehouse, database, schema)

print(session.sql('select current_warehouse(), current_database(), current_schema()').collect(), '\n')
print('Connected!\n')

session.sql("""create or replace table mytable(amount number comment 'fake amounts for testing', fruits string comment 'fake types of fruit for testing')""").show()
session.sql("""create or replace table mytable2 like mytable""").show()
session.sql("""insert into mytable values (1, 'apple'),(2, 'orange'),(5, 'grape'),(7, 'cantelope'),(9, 'pineapple'),(17, 'banana'),(21, 'tangerine')""").show()
session.sql("""insert into mytable2 values (1, 'apple'),(3, 'orange'),(5, 'grape'),(7, 'strawberry'),(10, 'pineapple'),(17, 'banana'),(22, 'raspberry')""").show()

def print_differences(session: snowflake.snowpark.Session, table1: str,table2: str,field1: str,field2: str):
    #read the tables into a snowpark dataframe
    table1 = session.table(table1)
    table2 = session.table(table2)

    #convert to pandas
    df1 = table1.to_pandas()
    df2 = table2.to_pandas()

    # convert the the fields of interest from each table to a list
    list1 = df1[field1].to_list()
    list2 = df2[field2].to_list()

    return ', '.join(item for item in list1 if item not in list2)

session.add_packages('snowflake-snowpark-python')

print('Registering Stored Procedure with Snowflake...\n')

session.sproc.register(
    func = print_differences
  , return_type = StringType()
  , input_types = [StringType(), StringType(), StringType(), StringType()]
  , is_permanent = True
  , name = 'PRINT_DIFFERENCES'
  , replace = True
  , stage_location = '@UDF_STAGE'
)

print('Stored Procedure registered with Snowflake!\n')

# You can return the results on one line using the sql() method:
# session.sql('''call print_differences('MYTABLE', 'MYTABLE2', 'FRUITS', 'FRUITS')''').show()

# Call stored procedure, print results as dataframe
x = session.call('print_differences', 'MYTABLE', 'MYTABLE2', 'FRUITS', 'FRUITS')
print(x, '\n')

df = pd.DataFrame({'Differences': x.split(',')})
print(df)