"""Title: Populate SQL Server Docker Container with production data
By: Martin Palkovic
Date: 2022-07-25
Description: Recently I had a need for a small, lightweight SQL Server development 
environment where I could play around with data and not impact anything in production.
This python script was my solution - it iteratively creates and populates tables 
in a test database that resides within a docker container.

Due to our Windows auth at work, I couldn't get this to run in a docker-compose 
file (i.e within the container). The solution is to run docker-compose to initialize 
SQL Server in the container, and then run this script locally

Exec in shell:
cd your/file/location
docker-compose up
python3 Populate_SQL_Server_Docker_Container.py
"""

#import modules
import pandas as pd
from sqlalchemy.engine import URL
from sqlalchemy import create_engine

#server credentials - prod
prod_server = 'prod_server'
prod_db = 'prod_db'

#server credentials - docker
docker_server = 'localhost'
docker_db = 'test_db'
username = 'sa' 
password = 'Your-Strong!Password@Here%'
#-------------------------
driver = 'SQL Server'
schema = 'dbo'

def sqlalchemy_cnxn(driver, server, db):
    connection = f"DRIVER={driver};SERVER={server};DATABASE={db}"
    url = URL.create("mssql+pyodbc", query={"odbc_connect": connection})
    engine = create_engine(url)
    return engine

# SQLAlchemy for Prod
prod_engine = sqlalchemy_cnxn(driver, prod_server, prod_db)

# SQLAlchemy for Docker
docker_engine = sqlalchemy_cnxn(driver, docker_server, docker_db)

docker_engine.execute('''
if not exists (select 1 from sys.databases where name = N'test_db')
create database test_db;
'''
)

"""create a list of each table in the database, 
and remove table names from the list that contain numbers 
(i.e duplicates/backups with dates on the end)
If you only want certain tables, you can manipulate this list however you like.
Only table names on this list will be queried from your prod database in the 
for loop below"""
prod_tables = [table for table in prod_engine.table_names()]
prod_tables = [i for i in prod_tables if not any(char.isdigit() for char in i)]

# This block is needed to connect to the db now that we have created it
docker_engine = sqlalchemy_cnxn(driver, docker_server, docker_db)

"""iterate over each table to populate the Docker container
Note that this takes ~1 min per 50 tables"""
for table in prod_tables:
    try:
        #read
        query = f'select top 1000 * from {prod_db}.{schema}.{table}'
        results = prod_engine.execute(query)
        df_sql = pd.read_sql(query, prod_engine)

        #write
        df_sql.to_sql(f'{table}', schema= f'{schema}', 
            con = docker_engine, chunksize=1, 
            index=False, if_exists='replace')
    except Exception:
        print(f'failed to insert {table} to docker container')