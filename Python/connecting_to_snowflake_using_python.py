""" Import Modules """
import os
from dotenv import load_dotenv
from snowflake import connector
# import pandas as pd

load_dotenv()

# establish connection to Snowflake using .env file
connection = connector.connect(
    user=os.getenv("SNOWFLAKE_USER"),
    password=os.getenv("SNOWFLAKE_PASSWORD"),
    account=os.getenv("SNOWFLAKE_ACCT"),
    role=os.getenv("SNOWFLAKE_ROLE"),
    warehouse="REPORTING_WH",
)

# sample SQL query, paste whatever you'd like in here
sql_query = "select * from database.schema.table limit 10;"

# execute the query
cursor = connection.cursor()
cursor.execute(sql_query)

# load the data in to Pandas
df = cursor.fetch_pandas_all()
df.head()
