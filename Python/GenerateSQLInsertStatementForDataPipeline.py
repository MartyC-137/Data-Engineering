"""
Script for printing out portions of a SQL insert statement for Boomi pipelines
By: Martin Palkovic
Date: 2022-06-23

In Boomi, I sometimes need to write cumbersome SQL insert statements. These are prone to human error 
and a great thing to automate. This script will print out the columns you need to insert into, 
as well as question marks for the variables.
"""

#import modules
import pandas as pd
from snowflake import connector

#establist connection to Cooke Snowflake warehouse
connection = connector.connect(user = 'your-username-here',
                              password = 'your-password-here',
                              account = 'sj12345.canada-central.azure',
                              role = 'SYSADMIN',
                              warehouse = 'REPORTING_WH')

#sample SQL query, paste whatever you'd like in here
database = 'my_db'
schema = 'dbo'
table = 'fact_salesordertransactions'
sql_query = f'select * from {database}.{schema}.{table} limit 5;'

#execute the query
cursor = connection.cursor()
cursor.execute(sql_query)

#load the data in to Pandas 
df = cursor.fetch_pandas_all()
# df.columns

# -----------------------------------
# initialize your Snowflake environment
print(f'use database {database};')
print(f'use schema {schema};')

# print columns for SQL insert statement
print(f'insert overwrite into {table}(')

for column in df.columns[:-1]:
        print(f"\"{column}\",")

print(f"\"{df.columns[-1]}\" \n)")
print('values')

# prints one ? for every column in the Snowflake table
for i in range(len(df.columns[:-1])):
    print('?,')
print('?')
print(');')