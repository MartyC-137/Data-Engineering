# **********************************************************************#
# Title: Basic Snowpark Example for backloading data to Snowflake
# By: Martin Palkovic
# Date: 2022-11-18
# Description: Recently I needed to backload some exchange rate data into Snowflake from
# SQL Server, and was excited because I got to test out Snowpark! It is a really nice
# way to interact with Snowflake using Python.
# *********************************************************************#

# Import modules
import os
from sqlalchemy.engine import URL
from sqlalchemy import create_engine

import pandas as pd

from snowflake.snowpark import Session

from dotenv import load_dotenv

load_dotenv()

# Establish SQL Server Connection
driver = "SQL Server"
server = "my_server"
database = "my_db"
schema = "dbo"
table = "Daily_Exchange_Rates"


# Define connection function
def sqlalchemy_cnxn(driver, server, db):
    connection = f"DRIVER={driver};SERVER={server};DATABASE={db}"
    url = URL.create("mssql+pyodbc", query={"odbc_connect": connection})
    engine = create_engine(url)
    return engine


engine = sqlalchemy_cnxn(driver, server, database)

# If you're not performing any data transformation at the
# SQL Server level, this is a great way to parameterize column names
columns = f"""SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_NAME LIKE N'{table}'"""

df_cols = pd.read_sql(columns, engine)
columns = ", ".join(df_cols["COLUMN_NAME"].to_list())

query = f"""SELECT {columns} FROM {database}.{schema}.{table}"""

# load query to dataframe
df_fx = pd.read_sql(query, engine)
print("Total records from SQL Server:", len(df_fx))

# --------------------------------------------

# Establish Snowpark Connection
account = os.getenv("SNOWFLAKE_ACCT")
user = os.getenv("SNOWFLAKE_USER")
password = os.getenv("SNOWFLAKE_PASSWORD")
role = os.getenv("SNOWFLAKE_ROLE")
warehouse = "REPORTING_WH"
database = "DEV"
schema = "MY_SCHEMA"
target_table = "CURRENCY_EXCHANGE_RATES"
temp_table = "FX_RATE_TEMP"


def snowpark_cnxn(account, user, password, role, warehouse, database, schema):
    connection_parameters = {
        "account": account,
        "user": user,
        "password": password,
        "role": role,
        "warehouse": warehouse,
        "database": database,
        "schema": schema,
    }
    session = Session.builder.configs(connection_parameters).create()
    return session


session = snowpark_cnxn(account, user, password, role, warehouse, database, schema)

print(
    session.sql(
        "select current_warehouse(), current_database(), current_schema()"
    ).collect()
)

# ---------------------------------------------------------------------

# Transform the data (if needed) to match the format that is required for Snowflake
# In my case, the data in the source data did not match what I needed
# for Snowflake.

df_sf = pd.DataFrame()

df_sf[["FROM_CURRENCY", "TO_CURRENCY"]] = df_fx["EXGTBLID_TRANSFORMED"].str.split(
    "-", 1, expand=True
)
df_sf = df_sf[
    df_sf["TO_CURRENCY"].str.contains("|".join(["AVG", "BUY", "SELL", "ALL"])) == False
]  # drops rows that contain junk data

df_sf["EFFECTIVE_START"] = df_fx["EXCHDATE"].dt.strftime("%Y-%m-%d %H:%m:%s.%S")
df_sf["EFFECTIVE_STOP"] = (
    df_fx["EXCHDATE"] + pd.DateOffset(days=7, hours=23, minutes=59)
).dt.strftime("%Y-%m-%d %H:%m:%s.%S")

df_sf["RATE"] = df_fx["XCHGRATE"]

# Get current datetime
df_sf["STAGE_DATE"] = pd.Timestamp.now()
df_sf["STAGE_DATE"] = df_sf["STAGE_DATE"].dt.strftime("%Y-%m-%d %H:%m:%s.%S")

# strip all whitespace from every field
df_sf = df_sf.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
print("Total records after transformations:", len(df_sf))

columns = ", ".join(df_sf.columns)

# Create Snowpark DataFrame
df = session.create_dataframe(df_sf)

df.write.mode("overwrite").save_as_table(
    f"{temp_table}", column_order="name", table_type="temporary"
)

session.sql(f"SELECT COUNT(*) FROM {temp_table}").collect()

# OPTION 1: Overwrite + insert new data
session.sql(
    f"""INSERT OVERWRITE INTO {target_table} ({columns})
            SELECT {columns} FROM {temp_table}"""
).collect()

# -------------------------------------------------------------

# OPTION 2: Incremental load
session.sql(
    f"""MERGE INTO {target_table} Dest
            USING (
                SELECT {columns} FROM {temp_table}
                QUALIFY ROW_NUMBER() OVER (
                    PARTITION BY MY_KEY
                    ORDER BY DATE ASC) = 1
                    ) Source
                    ON Dest.MY_KEY = Source.MY_KEY
                    AND Dest.FROM_CURRENCY = Source.FROM_CURRENCY
                    AND Dest.TO_CURRENCY = Source.TO_CURRENCY
            WHEN MATCHED THEN UPDATE
            SET   Dest.FROM_CURRENCY = Source.FROM_CURRENCY
                , Dest.TO_CURRENCY = Source.TO_CURRENCY
                , Dest.DATE = Source.DATE
                , Dest.RATE = Source.RATE
                , Dest.STAGE_DATE = Source.STAGE_DATE
            
            WHEN NOT MATCHED THEN INSERT(
                  FROM_CURRENCY
                , TO_CURRENCY
                , DATE
                , RATE
                , STAGE_DATE
            )
            VALUES(
                  Source.FROM_CURRENCY
                , Source.TO_CURRENCY
                , Source.EFFECTIVE_START
                , Source.RATE
                , Source.STAGE_DATE
            )
                """
).collect()
