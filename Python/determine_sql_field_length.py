"""Determing the maximum Length of a field for database table design
By: Martin Palkovic
Date: 2022-02-04

When building ETL/Integration jobs to Snowflake (or building any SQL table),
you need to designate how many characters are allowed in a field. I like to use
Python to quantitatively answer this question rather than manually counting or
guessing how many characters to allow in a varchar field """

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

"""stick your query inside the triple quotes"""

query = """SELECT * FROM <your_table_here>"""

#load query to dataframe
df_sql = pd.read_sql(query, cnxn)
df_sql.head()

"""Example"""
#Field of Interest
foi = 'Item_Key'
print('{} maximum record length ='.format(foi),
        max(df_sql[foi].astype(str).map(len)), 'characters')
# Output: Item_Key maximum record length = 19 characters

#Or run a for loop to get values for every column:
for c in df_sql.columns:
    print('{} maximum record length ='.format(c),
         max(df_sql[c].astype(str).map(len)), 'characters',
         'data type = {}'.format(df_sql[c].dtype))

#object == varchar
"""
Company maximum record length = 18 characters , data type = object
Company_Key maximum record length = 4 characters , data type = object
Site_Key maximum record length = 4 characters , data type = object
Item_Key maximum record length = 19 characters , data type = object
Item_Description maximum record length = 100 characters , data type = object
Species maximum record length = 15 characters , data type = object
Standard_Cost maximum record length = 8 characters , data type = float64
Current_Cost maximum record length = 8 characters , data type = float64
Category maximum record length = 16 characters , data type = object
Sub_Category maximum record length = 22 characters , data type = object
Size maximum record length = 8 characters , data type = object
Grade maximum record length = 7 characters , data type = object
Country_Of_Origin maximum record length = 15 characters , data type = object
Pallet maximum record length = 10 characters , data type = object
Bin maximum record length = 15 characters , data type = object
Order_Allocation maximum record length = 15 characters , data type = object
Production_Date maximum record length = 10 characters , data type = datetime64[ns]
Production_Age maximum record length = 4 characters , data type = int64
Lot_Date maximum record length = 10 characters , data type = datetime64[ns]
Lot_Age maximum record length = 7 characters , data type = float64
Weight maximum record length = 18 characters , data type = float64
Cases maximum record length = 9 characters , data type = float64
"""