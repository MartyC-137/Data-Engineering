import pandas as pd

csv = input('Enter filepath for the csv: ')

try:
    df = pd.read_csv(csv)

    file_name = input('Enter your file name (dont add the .json extension): ')
    df.to_json('{}.json'.format(file_name), orient = 'records')

except BaseException as exception:
    print(f'An exception occurred: {exception}')