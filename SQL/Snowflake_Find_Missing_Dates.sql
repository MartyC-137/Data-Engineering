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

WITH FIND_DATE_GAPS (ROWNUM, YOUR_DATE_FIELD) AS (
    SELECT
        YOUR_DATE_FIELD,
        ROW_NUMBER() OVER (ORDER BY YOUR_DATE_FIELD ASC) AS ROWNUM
    FROM YOUR_TABLE
    WHERE YOUR_DATE_FIELD > 'yyyy-mm-dd'
    GROUP BY YOUR_DATE_FIELD
)

SELECT
    DATEADD(DD, 1, A.YOUR_DATE_FIELD) AS STARTOFGAP,
    DATEADD(DD, -1, B.YOUR_DATE_FIELD) AS ENDOFGAP
FROM FIND_DATE_GAPS AS A
INNER JOIN FIND_DATE_GAPS AS B
    ON A.ROWNUM = (B.ROWNUM - 1)
WHERE DATEDIFF(DD, A.YOUR_DATE_FIELD, DATEADD(DD, -1, B.YOUR_DATE_FIELD)) != 0;
