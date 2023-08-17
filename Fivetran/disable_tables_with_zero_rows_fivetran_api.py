""" Import Modules """
import os
import json
import requests
import pandas as pd

from sqlalchemy.engine import URL
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

# Retrieve Fivetran secrets
fivetran_key = os.getenv("FIVETRAN_KEY")
fivetran_secret = os.getenv("FIVETRAN_SECRET")

# --------------------------------------------
""" Retrieve list of Fivetran connector IDs"""

# Define API variables
group_id = "my_fivetran_group_id"
url = "https://api.fivetran.com/v1/groups/" + group_id + "/connectors"
headers = {"Accept": "application/json"}

# API GET request
response = requests.get(url, headers=headers, auth=(fivetran_key, fivetran_secret))
data = response.json()

# Save Fivetran connector list to file
with open("fivetran_connector_list.json", "w") as file:
    json.dump(data, file, indent=4)

# Create a dictionary containing the database name(key) and connector ID(value)
connector_id_dict = {
    item["schema"].upper()
    if item["schema"] != "db_name_you_want_capitalized"
    else item["schema"].capitalize(): item["id"]
    for item in data["data"]["items"]
}

print(
    f"""Dictionary of connector ID's for Fivetran databases:
      {connector_id_dict} \n"""
)

# ------------------------------------------------------------------
""" Establish SQL Server Connection"""

# Define variables
driver = "SQL Server"
server = "my_server"

# Define connection function
def sqlalchemy_cnxn(driver, server, db):
    """ Function for connecting to SQL Server via SQLAlchemy """
    connection = f"DRIVER={driver};SERVER={server};DATABASE={db}"
    url = URL.create("mssql+pyodbc", query={"odbc_connect": connection})
    engine = create_engine(url)
    return engine

# ------------------------------------------------------------
""" Loop over list of databases/connector IDs to retrive tables
with 0 rows from SQL server, and call a PATCH request with the Fivetran API
to disable tables with 0 rows for that connector"""

for database in connector_id_dict.keys():
    engine = sqlalchemy_cnxn(driver, server, database)

    print(f"successfully connected to {server}.{database}!\n")
    print()  # new line

    # Query the sys schema for the database to get tables with 0 rows of data
    query = f"""
    SELECT
        t.NAME AS TableName,
        p.rows AS RowCounts
    FROM {database}.sys.tables AS t

    INNER JOIN {database}.sys.partitions AS p
        ON t.object_id = p.OBJECT_ID

    WHERE 
        t.NAME NOT LIKE 'dt%' 
        AND t.is_ms_shipped = 0
        AND p.rows = 0

    GROUP BY 
        t.Name, p.Rows

    ORDER BY 
        t.Name
    """

    # load results of query to Pandas dataframe
    df = pd.read_sql(query, engine)

    print(f"tables with 0 rows of data in {database} database: {len(df)}\n")

    tables_to_unsync = df["TableName"].tolist()

    # Create a JSON payload of tables to disable
    tables_payload = {table_name: {"enabled": False} for table_name in tables_to_unsync}
    payload = {"enabled": True, "tables": tables_payload}

    # For testing, if needed
    # with open(f"{database}_payload.json", "w") as file:
    #     json.dump(payload, file, indent = 4)

    # # ######################################
    """ Fivetran API Call to disable tables"""

    connector_id = connector_id_dict[database]
    print(f"Connector ID for {database}: {connector_id}\n")

    schema_name = "dbo"
    url = (
        "https://api.fivetran.com/v1/connectors/"
        + connector_id
        + "/schemas/"
        + schema_name
    )

    headers = {"Content-Type": "application/json", "Accept": "application/json"}

    """DO NOT UNCOMMENT THIS SECTION UNLESS YOU KNOW WHAT YOU'RE DOING"""
    response = requests.patch(url,
                              json = payload,
                              headers = headers,
                              auth = (fivetran_key, fivetran_secret))

    data = response.json()
    print(f"Successfully called the Fivetran API for the {connector_id} connector!\n")

    # For testing, if needed
    # with open('fivetran_api_response.json', 'w') as file:
    #     file.write(str(data))
    # print(f"Successfully saved logs to file!\n")

    # break #LEAVE THIS IN IF YOU ARE TESTING
