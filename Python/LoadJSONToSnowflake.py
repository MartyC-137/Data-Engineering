"""Example script to load multiple JSONs to a named Snowflake staging area, 
then copy the JSONs into a Snowflake table
By: Martin Palkovic
Date: 2022-07-28
Description: Sometimes in a dev environment, I need to manipulate a JSON file to see the effect that changes will have 
on my data pipeline. Here's a quick script I wrote to batch load json files into Snowflake, after I've altered some of the fields
"""

from snowflake import connector
import os
 
# folder containing your json files
root = r'C:\Users\martin.palkovic\source\repos\IT%20Department\Projects\Concur_NorthAmerica\JSON\CompanyCodeSwitch'

# Connect to your Snowflake account
cnxn = connector.connect(
    account = 'yj63875.canada-central.azure',
    user = 'your_username',
    password = 'your_password',
    role = 'STAGING_ADMIN',
    database = 'STAGING_DEV',
    schema = 'CONCUR',
    warehouse = 'REPORTING_WH'
    )

cursor = cnxn.cursor()
cursor.execute('create stage CONCUR;')
cursor.execute('use role SYSADMIN;')

for file in os.listdir(root):
    full_path = os.path.join(root, file)
    cursor.execute(f"put file://{full_path} @CONCUR;")

    copy_statement = file + '.gz'
    cursor.execute(f'''copy into CONCUR_EXPENSE_REPORTS (JSON_DATA) 
                from @concur/{copy_statement}
                file_format = (type = JSON);''')
cursor.close()
cnxn.close()