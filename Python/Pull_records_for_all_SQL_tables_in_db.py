"""Title: Data Pull for all views in SQL database
By: Martin Palkovic
Date: 2022-11-08
Description: Script to loop through every view in my_db and pull 100 records. 
The Business Analyst for a project at work asked for the structure of 
each my_db table, this was the fastest way to do it
"""

#import modules
from sqlalchemy.engine import URL
from sqlalchemy import create_engine

import pandas as pd

# SQL Server Connection - uses Active Directory to authenticate
driver = 'SQL Server'
server = 'my_server'
database = 'my_db'
schema = 'dbo'

# Define connection function
def sqlalchemy_cnxn(driver, server, db):
    connection = f"DRIVER={driver};SERVER={server};DATABASE={db}"
    url = URL.create("mssql+pyodbc", query={"odbc_connect": connection})
    engine = create_engine(url)
    return engine
engine = sqlalchemy_cnxn(driver, server, database)

list_of_views = 'SELECT name FROM sys.views'

my_server_views = pd.read_sql(list_of_views, engine)
list_of_sql_views = sorted(my_server_views['name'].to_list())
list_of_sql_views = [x for x in list_of_sql_views if x != 'DailySensorReadings'] #I had one table with 50M + rows that was causing performance issues, I removed it here

for view in list_of_sql_views:
    try:
        query = f'SELECT TOP 100 * FROM {database}.{schema}.{view}'
        results = engine.execute(query)
        df = pd.read_sql(query, engine)
        if len(df) > 0:
            df.to_csv(f'{view}.csv')
        else: 
            pass
    except Exception:
        print(f'failed to generate data for view {view}')