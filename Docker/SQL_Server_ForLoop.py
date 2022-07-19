#import modules
import pyodbc
from sqlalchemy.engine import URL
from sqlalchemy import create_engine
import pandas as pd

#server credentials - prod
prod_server = 'caisrv38'
prod_db = 'WH_BW'

#server credentials - docker
docker_server = 'localhost'
docker_db = 'test_db'
username = 'sa' 
password = '-xyKTjBx3Gk1k9zi5I39!'
#-------------------------
driver = 'ODBC Driver 17 for SQL Server'
schema = 'dbo'


#sql connection - prod 
prod_cnxn = pyodbc.connect(
    Trusted_Connection= 'Yes',
    Driver= '{SQL Server}',
    Server= prod_server,
    database= prod_db,
    user = username,
    password = password

)
cursor = prod_cnxn.cursor()

#docker connection
docker_cnxn = pyodbc.connect(
    # Trusted_Connection= 'Yes',
    Driver= '{SQL Server}',
    Server= docker_server,
    UID = username,
    PWD = password
    # database= db
)

docker_connection = f"DRIVER={driver};SERVER={docker_server};DATABASE={docker_db};UID={username};PWD={password}"
connection_url = URL.create("mssql+pyodbc", query={"odbc_connect": docker_connection})

engine = create_engine(connection_url, fast_executemany = True)

docker_cnxn.autocommit = True
docker_cnxn.execute('''
if not exists (select 1 from sys.databases where name = N'test_db')
create database test_db;
''')
docker_cnxn.autocommit = False

#create a list of each table in the database, and remove table names from the list that contain numbers (i.e duplicates/backups with dates on the end)
WH_BW_tables = [table.table_name for table in cursor.tables()]
WH_BW_tables = [item for item in WH_BW_tables if not any(character.isdigit() for character in item)]

#iterate over each table to populate the Docker container 
for table in WH_BW_tables[:10]:
    try:
        #read
        query = f'select top 1000 * from {prod_db}.{schema}.{table}'
        results = cursor.execute(query).fetchall()
        df_sql = pd.read_sql(query, prod_cnxn)

        #write
        df_sql.to_sql(f'{table}', schema= f'{schema}', 
            con = engine, chunksize=1, 
            index=False, if_exists='replace')
    except Exception:
        print(f'failed to insert {table} to docker container')