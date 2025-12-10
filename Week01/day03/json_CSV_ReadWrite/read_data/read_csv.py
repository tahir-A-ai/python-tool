import csv

file_path = 'json_CSV_ReadWrite\data\data.csv'

try:
    with open (file_path, 'r') as file:
        data = csv.reader(file)
        for row in data:
            print(row)  # this will output lists

except FileNotFoundError:
    print(f"error: file {file_path} not found!")

# in case the output needs to be in structure format i-e tabular form, use pandas

import pandas as pd
file_path = 'json_CSV_ReadWrite\data\data.csv'

try:
    with open (file_path, 'r') as file:
        data = pd.read_csv(file)
        print(data) # this will output in tabular format

except FileNotFoundError:
    print(f"error: file {file_path} not found!")