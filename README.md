# Data Engineering Portfolio

<div id="header" align="center">
    <img src="https://i.redd.it/w1m3or6z66j51.jpg" width="400"/>
</div>

[![forthebadge](https://forthebadge.com/images/badges/compatibility-pc-load-letter.svg)](https://forthebadge.com)
[![forthebadge](https://forthebadge.com/images/badges/kinda-sfw.svg)](https://forthebadge.com)
[![forthebadge](https://forthebadge.com/images/badges/approved-by-george-costanza.svg)](https://forthebadge.com)

[![Ruff](https://github.com/MartyC-137/Data-Engineering/actions/workflows/ruff.yml/badge.svg)](https://github.com/MartyC-137/Data-Engineering/actions/workflows/ruff.yml)
[![SQLFluff](https://github.com/MartyC-137/Data-Engineering/actions/workflows/sqlfluff.yml/badge.svg)](https://github.com/MartyC-137/Data-Engineering/actions/workflows/sqlfluff.yml)

---

### Introduction

This repository contains numerous work examples of code I use in my day to day work as a data engineer, all of which has been modified as minimum reproducible examples. My favourite tools are Snowflake, Python, and dbt, and I also have an interest in DevOps as it pertains to data engineering.

<div>
  <img src="https://github.com/devicons/devicon/blob/master/icons/python/python-original-wordmark.svg" title="Python" alt="Python" width="40" height="40"/>&nbsp;
  <img src = "https://upload.wikimedia.org/wikipedia/commons/thumb/f/ff/Snowflake_Logo.svg/2560px-Snowflake_Logo.svg.png" title="Snowflake" alt="Snowflake" width="150" height="40"/>&nbsp;
  <img src="https://seeklogo.com/images/D/dbt-logo-E4B0ED72A2-seeklogo.com.png" title="dbt" alt="dbt" width="100" height="40"/>&nbsp;
</div>

  [![Linkedin Badge](https://img.shields.io/badge/-Martin-blue?style=flat&logo=Linkedin&logoColor=white)](https://www.linkedin.com/in/mpalkovic/)

  [![Resume Badge](https://img.shields.io/badge/-Resume-blue?style=flat&logo=Resume&logoColor=white)](https://my.visualcv.com/martin-palkovic/)

---

### Table of Contents
* [Python Examples](https://github.com/MartyC-137/Data-Engineering/tree/main/Python)
    - [Snowpark example - backload data from SQL Server](https://github.com/MartyC-137/Data-Engineering/blob/main/Python/Snowpark_Example_Backload_Data.py)
    - [Snowpark example - backload data from API](https://github.com/MartyC-137/Data-Engineering/blob/main/Python/Snowpark_Backload_API_Data.py)
    - [Automated SQL insert statements from a CSV file](https://github.com/MartyC-137/Data-Engineering/blob/main/Python/Generate_SQL_Insert_Statements_From_CSV.py)
    - [Extract data from SQL Server, transform, and load to Snowflake](https://github.com/MartyC-137/Data-Engineering/blob/main/Python/Read_SQLServer_Write_Snowflake.py)
    - [Batch load JSON files to Snowflake](https://github.com/MartyC-137/Data-Engineering/blob/main/Python/LoadJSONToSnowflake.py)
    - [SQL Server data Pull - 100 Records from every view in a database](https://github.com/MartyC-137/Data-Engineering/blob/main/Python/Pull_records_for_all_SQL_tables_in_db.py)
* [SQL Examples](https://github.com/MartyC-137/Data-Engineering/tree/main/SQL)
    - [Auto Ingest Snowpipe from Azure Blob to Snowflake](https://github.com/MartyC-137/Data-Engineering/blob/main/SQL/Snowflake_Azure_Blob_Auto_Ingest_Snowpipe.sql)
    - [Shorten large union queries using Snowflake](https://github.com/MartyC-137/Data-Engineering/blob/main/SQL/Snowflake_Shorten_Huge_Union_Queries.sql)
    - [Flatten a JSON to a materialized view in Snowflake](https://github.com/MartyC-137/Data-Engineering/blob/main/SQL/Flatten_JSON_Window_Function_Example.sql)
    - [Basic Snowflake CDC Pipeline using Streams and Tasks](https://github.com/MartyC-137/Data-Engineering/blob/main/SQL/Snowflake_Basic_CDC_Pipeline_Using_Streams_Tasks.sql)
    - [Find missing dates in a date field - Snowflake](https://github.com/MartyC-137/Data-Engineering/blob/main/SQL/Find_Missing_Dates.sql)
    - [Snowflake data pipeline from internal stage](https://github.com/MartyC-137/Data-Engineering/blob/main/SQL/Snowflake_Data_Pipeline_From_Internal_Stage.sql)
* [Validate Snowflake code during a Pull Request using Azure Pipelines](https://github.com/MartyC-137/Data-Engineering/blob/main/Snowflake_Testing_Pipeline.yml)
* [Automated Snowflake deployments using Azure Pipelines](https://github.com/MartyC-137/Data-Engineering/blob/main/Snowflake_Deployment_Pipeline.yml)


---

### Usage

```bash
# Clone the repository
git clone https://github.com/MartyC-137/Data-Engineering.git

# Connect to the repository
cd Data-Engineering
```
