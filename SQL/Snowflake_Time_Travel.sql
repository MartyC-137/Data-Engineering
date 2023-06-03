/* Title: Snowflake Time Travel
By: Martin Palkovic
Date: 2022-06-07
Description: Snowflake has great time travel functionality, were you can easily restore
a table to its state at a previous point in time. I have used this functionality with
great success when a production table with 2 million records was deleted on accident!
*/

show tables history;

/* Note that you may need to rename the table */
alter table my_table rename to my_table_whoops;

/* specify the time */
select 
      acct_number
    , date 
    from db.schema.my_table
    at (timestamp => '2022-06-01 6:00');

/* specify an offset, ex. 1 hour ago*/
select
      acct_number,
      date 
    from db.schema.my_table
    at (offset => -60*60); --offset is in seconds here
