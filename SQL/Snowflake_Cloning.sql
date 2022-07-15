/* How to clone data in Snowflake
By: Martin Palkovic
Date: 2022-06-10 

Description: Zero copy cloning is one of the awesome features of Snowflake. 
I like to use this feature to quickly create a development environment for 
testing */

use role sysadmin;
use warehouse reporting_wh;
use database production;
use schema dbo;

/* clone database */
create database my_cloned_db clone my_db;

/* clone schema */
create schema my_cloned_schema clone analytics_inventory;

/* clone table */
create table my_cloned_table clone main_inventory_table;

/* cloning with time travel  */
create or replace table my_cloned_table clone main_inventory_table
at (timestamp => '2022-06-10 9:30')