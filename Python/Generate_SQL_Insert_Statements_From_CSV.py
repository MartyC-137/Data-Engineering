"""Generate a SQL insert statement from a csv file
By: Martin Palkovic
Date: 2022-03-14"""

import pandas as pd

#Filepath for the csv
df = pd.read_csv('my_file.csv')

#In my case I only wanted after row 1022
df = df.iloc[1022:]

#There are some weird unicode characters in the excel sheet I received,
#I removed them with this for loop:
for column in df.columns:
    df[column] = df[column].str.split().str.join(' ')

#Define Function
def sql_insert_statement_from_dataframe(source, target):
    sql_texts = []
    for index, row in source.iterrows():
        #full insert statement:
        print('insert into ' + target + '(' + str(', '.join(source.columns)) + ') values ' + str(tuple(row.values)) + ';')

        #just the values portion:
#         print(str(tuple(row.values)) + ',')

    return None

#Execute Function
sql_insert_statement_from_dataframe(df, 'database.schema.table')
"""
#Full insert statement:
insert into database.schema.table(code, expense_type, acct, company) values ('02113', 'Accounts Receivable, Other', '35400', 'An_Awesome_Company');
insert into database.schema.table(code, expense_type, acct, company) values ('02114', 'Accounts Payable', '36500', 'A_Different_Company');
insert into database.schema.table(code, expense_type, acct, company) values ('02115', 'Donations', '12220', 'Another_Company');

#just the values:
('02113', 'Accounts Receivable, Other', '35400', 'An_Awesome_Company'),
('02114', 'Accounts Payable', '36500', 'A_Different_Company'),
('02115', 'Donations', '12220', 'Another_Company'),
"""