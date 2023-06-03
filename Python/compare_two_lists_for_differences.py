"""Compare two lists for differences
By: Martin Palkovic
Date: 2022-02-09"""
# ------------------------------
# a common work task is to compare two database ID fields
# against each other to determine which records exist
# in one table but not another. This operation can take 10+
# minutes to run in SQl and is syntactically heavy, but is
# fast and easy in Python.


# Copy and paste your fields below
# to identify records that are unique to one of the tables

list1 = ["red", "blue", "yellow", 7, 25]  # copy and paste your values into here
list2 = ["yellow", 7, "blue", 1, 5.4]

# returns items that are in list1 but not in list2 - adjust accordingly to suit your needs
list_difference = [item for item in list1 if item not in list2]
list_difference
