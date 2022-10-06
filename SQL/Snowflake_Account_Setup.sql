/******************************************************************************/
-- Script: Account Setup in Snowflake
-- CreateBy: Martin Palkovic
-- Create date: 2022-11-01
-- Description: Script to set up a warehouse, role and user with basic privileges
/******************************************************************************/

/* Set session variables*/
set role_name = 'my_role';
set user_name = 'my_user';
set wh_name = 'my_warehouse';
set db_name = 'my_db';

/* Create warehouse for service account */
use role sysadmin;
create or replace warehouse identifier($wh_name)
warehouse_size = xsmall
auto_suspend = 60
auto_resume = true
min_cluster_count = 1
max_cluster_count = 5
scaling_policy = standard
comment = 'Warehouse for service account to query the Snowflake API';

/* Create role */
use role securityadmin;
create or replace role identifier($role_name)
comment = 'Default role for service account my_user';

/* Create user */
use role accountadmin;
create or replace user identifier($user_name)
login_name = $user_name
display_name = $user_name
password = '********************'
must_change_password = false
default_role = $role_name
default_warehouse = $wh_name
comment = 'Service account for application to query the Snowflake API';

/* grant account permissions */
grant role identifier($role_name) to user identifier($user_name);
grant usage on warehouse identifier($wh_name) to role identifier($role_name);
grant usage on database identifier($db_name) to role identifier($role_name);
grant usage on all schemas in database identifier($db_name) to role identifier($role_name);
grant select on all tables in database identifier($db_name) to role identifier($role_name);

/* Future Grants */
grant select on future tables in database identifier($db_name) to role identifier($role_name);
grant usage on future schemas in database identifier($db_name) to role identifier($role_name);

/* Confirm access is correct */
show grants to role identifier($role_name);

show grants of role identifier($role_name);
show grants to user identifier($user_name);