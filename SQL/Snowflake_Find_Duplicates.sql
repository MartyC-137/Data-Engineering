select * from my_table
qualify count(*) over (partition by primary_key) > 1;
