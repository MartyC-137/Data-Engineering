/* Script for preventing duplicate JSON data from entering Snowflake during ELT
By Martin Palkovic
2022-03-23
 */
select 1 from dbo.table where ? in
(select dir.value:Id::String
from staging_dev.dbo.table,
lateral flatten (input => JSON_DATA: Workorders) dir
);
