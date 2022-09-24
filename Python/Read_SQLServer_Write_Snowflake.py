"""Script to read data from SQL Server and write it to Snowflake
By: Martin Palkovic
Date: 2022-09-14
Description: For a work task, I needed to add some historical exchange rate data 
to Snowflake for analytical reporting. This data existed on SQL server, so I wrote this
Python script to read the data from SQL Server, transform it, and load it into Snowflake.
I've modified this as a minimum reproducable example for the purposes of my project portfolio.
"""

"""Step 1: Read data from SQL Server"""

#import modules
import os, pyodbc
import pandas as pd
from snowflake import connector

#set all rows and columns visible
#pd.set_option('display.max_columns', None)
#pd.set_option('display.max_rows', None)

#server credentials
server = 'my_server'
database = 'my_database'

#sql connection
cnxn = pyodbc.connect(
    Trusted_Connection= 'Yes',
    Driver= '{SQL Server}',
    Server= server,
    Database= database
)
cursor = cnxn.cursor()

#stick your query inside the triple quotes
query = """select * from DATABASE.SCHEMA.EXCHANGERATES where EXCHDATE > '2021-09-03' and EXCHDATE < '2021-09-09' order by EXCHDATE asc"""

#load query to dataframe
df_fx = pd.read_sql(query, cnxn)
print(df_fx.dtypes)

# --------------------------------------------------------

"""Step 2: Create a dataframe that matches the Snowflake table we are inserting to"""
df_sf = pd.DataFrame()

# Create the from and to currency columns
df_sf[['FROM_CURRENCY', 'TO_CURRENCY']] = df_fx['EXCHANGE_ID'].str.split('-', 1, expand = True)
df_sf = df_sf[df_sf['TO_CURRENCY'].str.contains('AVG') == False] #drops rows that show avg - there are some GBP AVG

# Create the start and stop date columns
df_sf['EFFECTIVE_START'] = df_fx['EXCHDATE'].dt.strftime('%Y-%m-%d %H:%m:%s.%S')
df_sf['EFFECTIVE_STOP'] = (df_fx['EXCHDATE'] + pd.DateOffset(days = 7, hours = 23, minutes = 59)).dt.strftime('%Y-%m-%d %H:%m:%s.%S')

# Exchange Rate
df_sf['RATE'] = df_fx['XCHGRATE']

# Get current datetime
df_sf['STAGE_DATE'] = pd.Timestamp.now()

# strip all whitespace from every field
df_sf = df_sf.apply(lambda x: x.str.strip() if x.dtype == 'object' else x)

# diagnostic check...number of rows, data types etc.
print('Number of rows:', len(df_sf))
print(df_sf.dtypes)
# print(df_sf.head())
df_sf.to_csv('FXRates.csv', header = False, index = False)

# ------------------------------------------------------------------
"""Step 3: Write data to Snowflake """
#Establish connection to Cooke Snowflake 
cnxn = connector.connect(user = 'your_snowflake_account',
                              password = 'your_password',
                              account = 'ab12345.canada-central.azure',
                              role = 'SYSADMIN',
                              warehouse = 'REPORTING_WH')

# assign csv to variable
csv = r'<your_filepath_here>\FXRates.csv.csv'
staged_file = os.path.basename(csv) + '.gz'

#execute write operations
cursor = cnxn.cursor()
cursor.execute('use database STAGING_DEV;')
cursor.execute('use schema MY_SCHEMA;')
cursor.execute('create or replace stage FX_RATES;')
cursor.execute(f'put file://{csv} @FX_RATES;')
cursor.execute(f'''copy into CURRENCY_EXCHANGE_RATES(FROM_CURRENCY, TO_CURRENCY, EFFECTIVE_START, EFFECTIVE_STOP, RATE, STAGE_DATE)
               from @FX_RATES/{staged_file}
               file_format = (type = CSV)''')
cursor.execute('remove @MY_SCHEMA.FX_RATES pattern = ".*FX_RATES.*";')

cursor.close()
cnxn.close()