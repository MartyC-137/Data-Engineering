/* Query: find missing dates in a range of dates
By: Martin Palkovic
Date: 2022-08-19
System: Snowflake
Description: Say, for example, you have a report, and there is data missing for certain dates
on that report. You can use this query to identify dates where you may have missing data
 */

USE ROLE SYSADMIN;
USE WAREHOUSE REPORTING_WH;
USE DATABASE YOUR_DB;
USE SCHEMA YOUR_SCHEMA;

WITH find_date_gaps(RowNum, your_date_field) AS 
(
   SELECT ROW_NUMBER() OVER(ORDER BY your_date_field ASC) AS RowNum, your_date_field
        FROM YOUR_TABLE
        WHERE your_date_field > 'yyyy-mm-dd'
        GROUP BY your_date_field
)
SELECT 
    DATEADD(dd, 1, a.your_date_field) AS startOfGap 
    , DATEADD(dd, -1, b.your_date_field) AS endOfGap
    FROM find_date_gaps a 
    JOIN find_date_gaps b
        ON a.RowNum = (b.RowNum - 1)
    WHERE DATEDIFF(dd, a.your_date_field, DATEADD(dd, -1, b.your_date_field)) != 0;