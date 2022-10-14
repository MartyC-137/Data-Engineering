"""Example script to load multiple JSONs to a named Snowflake staging area, 
then copy the JSONs into a Snowflake table
By: Martin Palkovic
Date: 2022-07-28
Description: Sometimes in a dev environment, I need to manipulate a JSON file to see the effect that changes will have 
on my data pipeline. Here's a quick script I wrote to batch load json files into Snowflake, after I've altered some of the fields
"""

import os
from snowflake import connector

# folder containing your json files
root = r'C:\Directory\containing\JSON\files'

# Connect to your Snowflake account
cnxn = connector.connect(
    account = 'ab12345.canada-central.azure',
    user = 'your_username',
    password = 'your_password',
    role = 'sysadmin',
    database = 'dev',
    schema = 'dbo',
    warehouse = 'reporting_wh'
    )

cursor = cnxn.cursor()
cursor.execute('create or replace stage MY_STAGE;')
cursor.execute('use role SYSADMIN;')

for file in os.listdir(root):
    full_path = os.path.join(root, file)
    cursor.execute(f"put file://{full_path} @MY_STAGE;")

    copy_statement = file + '.gz'
    cursor.execute(f'''copy into EXAMPLE_TABLE (JSON_DATA, INSERT DATE) 
                from (select t.$1, current_timestamp() from @MY_STAGE/{copy_statement} t)
                file_format = (type = JSON);''')
cursor.close()
cnxn.close()