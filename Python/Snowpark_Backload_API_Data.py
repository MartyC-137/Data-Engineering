# **********************************************************************#
# Title: Backload API data using Snowpark Python
# By: Martin Palkovic
# Date: 2022-11-18
# Description: Here is another Snowpark example, where you can loop through
# an API call and insert the JSON response for each days worth of data
# into a VARIANT table in Snowflake
# *********************************************************************#

# Import modules
import json, requests

from datetime import date, timedelta
from snowflake.snowpark import Session

# Establish Snowflake Connection using Snowpark
account = 'xy45678.canada-central.azure'
user = 'my_user'
password = 'my_password'
role = 'SYSADMIN'
warehouse = 'REPORTING_WH'
database = 'DEV'
schema = 'MY_SCHEMA'
target_table = 'MY_TABLE'

def snowpark_cnxn(account, user, password, role, warehouse, database, schema):
    connection_parameters = {
    "account": account,
    "user": user,
    "password": password,
    "role": role,
    "warehouse": warehouse,
    "database": database,
    "schema": schema
   }
    session = Session.builder.configs(connection_parameters).create()
    return session

session = snowpark_cnxn(account,
                        user,
                        password,
                        role,
                        warehouse,
                        database,
                        schema)

print(session.sql('select current_warehouse(), current_database(), current_schema()').collect())

# API variables
headers = {
  'APIKey': 'Your_API_key_here'
}

# Define a function so we can loop over a date range
def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)
        
start_date = date(2019, 1, 1)
end_date = date(2022, 11, 18)

# Loop through 3 years worth of API data, insert into Snowflake VARIANT table
for date in daterange(start_date, end_date):
    url = f'https://api.mywebsite.com/api/data?&startDate={date}&endDate={date}'
    response = requests.request("GET", url, headers=headers)
    
    formatted_json = json.loads(response.text)
    formatted_json = json.dumps(formatted_json, indent = 4)
    
    # insert to Snowflake
    session.sql(f'''INSERT INTO {target_table} (JSON_DATA, INSERT_DATE)
                    SELECT PARSE_JSON('{formatted_json}'),
                    CURRENT_TIMESTAMP();''').collect()