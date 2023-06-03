/**********************************************************************/
-- Title: Azure Blob Snowpipe setup
-- By: Martin Palkovic
-- Date: 2022-11-09
-- Description: Snowflake set up of an auto-ingest snowpipe from Azure Blob Storage to Snowflake table.
-- Documentation: https://docs.snowflake.com/en/user-guide/data-load-snowpipe-auto-azure.html
/*********************************************************************/

/* Set session variables */
set session_role = 'sysadmin';
set session_warehouse = 'reporting_wh';
set session_database = 'dev';
set session_table = 'my_table';
set project_name = 'MY_PROJECT';
set storage_loc = 'azure://your_blob_account_here.blob.core.windows.net/my_project';
set tenant_id = 'a123b4c5-1234-123a-a12b-1a23b45678c9'; -- example tenant id from Snowflake docs

/* Initialize Environment */
use role identifier($session_role);
use warehouse identifier($session_warehouse);
use database identifier($session_database);

create schema if not exists identifier($project_name);
use schema identifier($project_name);

/* Create storage integration for Snowflake to connect to Azure Blob.
See the 'Configuring Secure Access to Cloud Storage' section in the url above*/
create storage integration if not exists identifier($project_name)
type = external_stage
storage_provider = 'AZURE'
enabled = true 
azure_tenant_id = $tenant_id
storage_allowed_locations = ($storage_loc)
comment = 'Storage Integration for moving my_project data into Snowflake';

/* The output of this command is needed for setup in the Azure Portal */
desc storage integration identifier($project_name);

/* Create notification integration to connect Snowflake to Azure Event Grid.
See Step 2 of 'Configuring Automation With Azure Event Grid'*/
create notification integration if not exists identifier($project_name)
enabled = true
type = queue
notification_provider = azure_storage_queue
azure_storage_queue_primary_uri = '<queue_URL>'
azure_tenant_id = $tenant_id
comment = 'Notification Integration for moving my_project data into Snowflake';

/* The output of this command is needed for setup in the Azure Portal */
desc notification integration identifier($project_name);

/* Create a Snowflake stage */
create stage if not exists identifier($project_name)
url = $storage_loc
storage_integration = $project_name
comment = 'Staging area for my_project data, between Azure Blob and Snowflake';

-- show stages;

/* Create a Snowpipe that will be notified via Azure Event Grid 
when a file is added to the Azure Blob instance specified above*/
create pipe if not exists identifier($project_name)
auto_ingest = true
integration = $project_name
as
copy into $session_table
from @$project_name
file_format = (type = 'csv')
comment = 'Auto Ingest Snowpipe for moving data from Azure Blob to Snowflake. When a file is added to
Azure Blob, this Snowpipe will automatically trigger';
