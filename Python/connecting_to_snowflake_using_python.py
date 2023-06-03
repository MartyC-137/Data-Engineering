"""Quickstart guide for querying snowflake using Python
Author: Martin Palkovic
Date: 2022-02-03"""

"""run these two lines if this is your first time
connecting to snowflake through Python"""
# pip install snowflake-connector-python
# pip install pyarrow==5.0.0

# import modules
import os
import pandas as pd
from snowflake import connector

from dotenv import load_dotenv

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
