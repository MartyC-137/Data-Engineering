--Total number of Null and Non-Null values 
select 
    sum(case 
            when [your_field_here] is null then 1 
            else 0 
            end) as [Number of Null Values]
        , count([your_field_here]) as [Number of Non-Null Values]
    from database.schema.table

--Percentage of Non-Null Values
select 
    cast(x.non_nulls as float) / cast(y.nulls as float) * 100  
    as [Percentage of Non-Null Values]
    from
    (
        select 
        count([your_field_here]) as non_nulls
        from database.schema.table
    ) x 
    join
    (
        select 
        sum(case when [your_field_here] is null then 1 else 0 end) as nulls
        from database.schema.table
    ) y 
    on 1 = 1
