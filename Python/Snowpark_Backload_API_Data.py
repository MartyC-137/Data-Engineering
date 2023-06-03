# **********************************************************************#
# Title: Backload API data using Snowpark Python
# By: Martin Palkovic
# Date: 2022-11-18
# Description: Here is another Snowpark example, where you can loop through
# an API call and insert the JSON response for each days worth of data
# into a VARIANT table in Snowflake
# *********************************************************************#

# Import modules
import os
import json
import requests

from datetime import date, timedelta
from snowflake.snowpark import Session

from dotenv import load_dotenv

load_dotenv()

# Establish Snowflake Connection using Snowpark
account = os.getenv("SNOWFLAKE_ACCT")
user = os.getenv("SNOWFLAKE_USER")
password = os.getenv("SNOWFLAKE_PASSWORD")
role = os.getenv("SNOWFLAKE_ROLE")
role = "SYSADMIN"
warehouse = "MY_WH"
database = "DEV"
schema = "MY_SCHEMA"
target_table = "MY_TABLE"

api_key = os.getenv("MY_API_KEY")


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
        "SELECT CURRENT_WAREHOUSE(), CURRENT_DATABASE(), CURRENT_SCHEMA()"
    ).collect()
)

# API variables
headers = {"APIKey": f"{api_key}"}


# Define a function so we can loop over a date range
def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)


start_date = date(2019, 1, 1)
end_date = date(2022, 11, 18)

# Loop through 4 years worth of API data, insert into Snowflake VARIANT table
for dates in daterange(start_date, end_date):
    url = f"https://api.mywebsite.com/api/data?&startDate={date}&endDate={date}"
    response = requests.request("GET", url, headers=headers)

    formatted_json = json.loads(response.text)
    formatted_json = json.dumps(formatted_json, indent=4)

    # insert to Snowflake
    session.sql(
        f"""INSERT INTO {target_table} (JSON_DATA, INSERT_DATE)
                    SELECT PARSE_JSON('{formatted_json}'),
                    CURRENT_TIMESTAMP();"""
    ).collect()
