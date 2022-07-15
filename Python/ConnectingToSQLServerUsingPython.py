#import modules
import pyodbc
import pandas as pd

#set all rows and columns visible
#pd.set_option('display.max_columns', None)
#pd.set_option('display.max_rows', None)


#server credentials
server = 'server'
database = 'database'

#sql connection
cnxn = pyodbc.connect(
    Trusted_Connection= 'Yes',
    Driver= '{SQL Server}',
    Server= server,
    Database= database
)
cursor = cnxn.cursor()

#stick your query inside the triple quotes
query = """select top 10 * from database.dbo.table"""

#load query to dataframe
df_sql = pd.read_sql(query, cnxn)
df_sql.head()