"""SQL Insert statement from dataframe
By: Martin Palkovic
Date: 2022-03-15"""

import pandas as pd

dataframe = pd.read_csv('my_file.csv')

def sql_insert_statement_from_dataframe(source, target):
    print('insert into ' + target + '(' + str(', '.join(source.columns)) + ') \nvalues')

    for index, row in source.iterrows():
        print(str(tuple(row.values)) + ',')

    return None

sql_insert_statement_from_dataframe(dataframe, 'database.schema.table')

Output:
insert into database.schema.table(Amount, Account_Name, Account_Number, Company)
values
('02113', 'Accounts Receivable, Other', '35400', 'An_Awesome_Company'),
('02114', 'Accounts Payable', '36500', 'A_Different_Company'),
('02115', 'Donations', '12220', 'Another_Company')
