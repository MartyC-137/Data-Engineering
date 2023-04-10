import pandas as pd
import numpy as np

df = pd.read_csv(r"your/file/here.csv")
df = df.replace({np.nan: 'NULL'})

print('successfully read csv!\n')

def sql_insert_statement_from_dataframe(source, target):
    print('insert into ' + target + '(' + str(', '.join(source.columns)) + ') values ')
    for i, x in source.iterrows():
        values = x.values
        formatted_values = []
        for val in values:
            if val == 'NULL':
                formatted_values.append(val)
            else:
                formatted_values.append("'" + str(val) + "'")
        if i == len(source) -1:
            print( '(' + str(', '.join(formatted_values)) + ');')
        else:
            print( '(' + str(', '.join(formatted_values)) + '),')
            
sql_insert_statement_from_dataframe(df, 'my_db.my_schema.my_table')