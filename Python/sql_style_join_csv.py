"""Performing a SQL style join on two csv files
By: Martin Palkovic
Date: 2022-02-11

Description: The inventory team is producing Excel sheets on a weekly basis
and would like to move comments from one sheet to another. Inventory goes out,
new inventory comes in, and they want the comments transfered on items that are
still in stock. I wasn't sure how to do this in SQL without making new tables
in the database and decided to use Python.

Note that this program is specific to a workflow I do for the Inventory team,
and you cant really make a one size fits all program for this task since you
need to specify which fields you want to join. But hopefully it will give you
an idea of how to do this if you encounter a similar task
"""

import os
import pandas as pd

old_csv = input("Enter filepath for the old csv: ")
while not os.path.isfile(old_csv):
    print("Error: that is not a valid file, try again...")
    old_csv = input("Enter filepath for the old csv: ")

new_csv = input("Enter filepath for the new csv: ")
while not os.path.isfile(new_csv):
    print("Error: that is not a valid file, try again...")
    new_csv = input("Enter filepath for the new csv: ")

try:
    df_old = pd.read_csv(old_csv, low_memory=False)
    df_new = pd.read_csv(new_csv, low_memory=False)

    # makes all column names lower case, ensuring they meet the join criteria
    # i.e if the user capitalizes one of the column names one week but not the next,
    # it doesn't matter with this block of code
    df_old.columns = map(str.lower, df_old.columns)
    df_new.columns = map(str.lower, df_new.columns)

    # removes any whitespace from the column names
    df_old = df_old.rename(columns=lambda x: x.strip())
    df_new = df_new.rename(columns=lambda x: x.strip())

    df_old = df_old.loc[:, df_old.columns.isin(["columns_you_want_to_keep"])]
    df_old = df_old.reset_index(drop=True)

    df_new = df_new.loc[:, ~df_new.columns.isin(["columns_you_want_to_keep"])]
    df_new = df_new.reset_index(drop=True)

    df = pd.merge(
        df_new,
        df_old.drop_duplicates(subset=["pallet"]),
        how="left",
        on=["pallet"],
        suffixes=("", "_drop"),
    )

    df = df.drop([c for c in df.columns if "drop" in c], axis=1)
    df.columns = map(str.capitalize, df.columns)

    file_name = input("Enter your file name (dont add the .csv extension): ")
    df.to_csv("{}.csv".format(file_name))

except BaseException as exception:
    print(f"An exception occurred: {exception}")
