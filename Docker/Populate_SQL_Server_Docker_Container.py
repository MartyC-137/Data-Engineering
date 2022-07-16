"""Title: Populate SQL Server Docker Container with production data
By: Martin Palkovic
Date: 2022-07-15
Description: Recently I had a need for a small, lightweight SQL Server development environment where I could play around with data
and not impact anything in production. This python script was my solution - it iteratively creates and populates tables in a test database
that resides within a docker container"""

#import modules
import pyodbc
from sqlalchemy.engine import URL
from sqlalchemy import create_engine
import pandas as pd

#server credentials
prod_server = 'my_production_server'
prod_db = 'my_prod_db'
prod_schema = 'dbo'
docker_server = 'localhost'
docker_db = 'my_prod_db'
docker_schema = 'dbo'
username = 'sa' 
password = '<your_strong_password_here>' 


#sql connection - prod 
prod_cnxn = pyodbc.connect(
    Trusted_Connection= 'Yes',
    Driver= '{SQL Server}',
    Server= prod_server,
    database= prod_db,

)
cursor = prod_cnxn.cursor()

#sql connection - docker 
docker_cnxn = pyodbc.connect(
    Driver= '{SQL Server}',
    Server= docker_server,
    UID = username,
    PWD = password
    # database= db
)

docker_connection = "DRIVER={ODBC Driver 17 for SQL Server};SERVER=localhost;DATABASE=test_db;UID=sa;PWD=<your_strong_password_here>"
connection_url = URL.create("mssql+pyodbc", 
                            query={"odbc_connect": docker_connection})

engine = create_engine(connection_url, fast_executemany = True)

#-----------------------------------------------

docker_cnxn.autocommit = True
docker_cnxn.execute('''
if not exists (select 1 from sys.databases where name = N'test_db')
create database test_db;
''')
docker_cnxn.autocommit = False

#create a list of each table in the database, and remove table names from the list that contain numbers (i.e duplicates/backups with dates on the end)
my_prod_db_tables = [table.table_name for table in cursor.tables()]
my_prod_db_tables = [item for item in my_prod_db_tables if not any(char.isdigit() for char in item)]

#iterate over each table to populate the Docker container 
for table in my_prod_db_tables:
    try:
        #read
        query = f'select top 1000 * from {prod_db}.{prod_schema}.{table}'
        results = cursor.execute(query).fetchall()
        df_sql = pd.read_sql(query, prod_cnxn)

        #write
        df_sql.to_sql(f'{table}', schema= f'{docker_schema}', 
                    con = engine, chunksize = 1000, 
                    index = False, if_exists = 'replace')
    except Exception:
        print(f'failed to insert {table} to docker container')