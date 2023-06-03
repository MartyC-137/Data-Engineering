/* Title: Example MERGE INTO statement for incremental loading into Snowflake
By: Martin Palkovic
Date: 2022-10-20
Description: With large datasets, you'll often want to implement an incremental load to
improve performance in your data pipeline. The code below will prevent duplicates in your load,
while only adding new records and updating existing records if changes exist. Note that this code excludes
the database name from the full qualified table name - that is deliberate so that this code can be run against
a development database first. The database name is set in the environment extensions of your pipeline tool.

-- This is a minimum reproducible example of code I've used in production.
*/

merge into
    my_schema.my_table as destination

using (
    select *
    from my_schema.my_staging_table
    qualify row_number() over (
        partition by my_unique_sk
        order by created_date desc
    ) = 1
) as source
    on (source.my_unique_sk = destination.my_unique_sk)

when matched then
    update
    set
        destination.my_unique_sk = source.my_unique_sk,
        destination.order_id = source.order_id,
        destination.ship_date = source.ship_date

when not matched
then insert
    (
        my_unique_sk,
        order_id,
        ship_date
    )
values
(
    source.my_unique_sk,
    source.order_id,
    source.ship_date
);
