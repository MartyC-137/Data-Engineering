SELECT * FROM database.schema.table
QUALIFY COUNT(*) OVER (PARTITION BY primary_key) > 1;