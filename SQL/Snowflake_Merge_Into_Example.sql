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

MERGE INTO 
my_schema.my_table Destination

USING (
    SELECT * 
    FROM my_schema.my_staging_table
    QUALIFY ROW_NUMBER() OVER (
        PARTITION BY my_unique_sk
        ORDER BY created_date DESC
    ) = 1
) Source
    ON (Source.my_unique_sk = Destination.my_unique_sk) 

WHEN MATCHED THEN UPDATE 
SET 
Destination.my_unique_sk=Source.my_unique_sk
, Destination.order_id=Source.order_id
, Destination.ship_date=Source.ship_date

WHEN NOT MATCHED 
THEN INSERT
(my_unique_sk
, order_id
, ship_date
) 
VALUES 
(Source.my_unique_sk
, Source.order_id
, Source.ship_date);