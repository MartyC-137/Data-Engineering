/* Query: find missing dates in a range of dates
By: Martin Palkovic
Date: 2022-08-19
System: Snowflake
Description: Say, for example, you have a report, and there is data missing for certain dates
on that report. You can use this query to identify dates where you may have missing data
 */

use role sysadmin;
use warehouse my_warehouse;
use database my_db;
use schema my_schema;

with find_date_gaps (rownum, your_date_field) as (
    select
        your_date_field,
        row_number() over (order by your_date_field asc) as rownum
    from your_table
    where your_date_field > 'yyyy-mm-dd'
    group by your_date_field
)

select
    dateadd(dd, 1, fdg1.your_date_field) as startofgap,
    dateadd(dd, -1, fdg2.your_date_field) as endofgap
from find_date_gaps as fdg1
inner join find_date_gaps as fdg2
    on a.rownum = (b.rownum - 1)
where datediff(dd, a.your_date_field, dateadd(dd, -1, b.your_date_field)) != 0;
