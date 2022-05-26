"""Quickstart guide for querying snowflake using Python
Author: Martin Palkovic
Date: 2022-02-03"""

"""run these two lines if this is your first time
connecting to snowflake through Python"""
#pip install snowflake-connector-python
#pip install pyarrow==5.0.0

#import modules
import pandas as pd
from snowflake import connector

#establist connection to Cooke Snowflake warehouse
connection = connector.connect(user = 'your_username_here',
                              password = 'your_password_here',
                              account = 'ex12345.canada-central.azure',
                              role = 'SYSADMIN',
                              warehouse = 'REPORTING_WH')

#sample SQL query, paste whatever you'd like in here
sql_query = 'select * from database.schema.table limit 10;'

#execute the query
cursor = connection.cursor()
cursor.execute(sql_query)

#load the data in to Pandas 
df = cursor.fetch_pandas_all()
df.head()
