import csv

file_path = 'json_CSV_ReadWrite\data\data.csv'
new_student = ['Umer', 'C']

try:
    with open(file_path, 'a', newline='') as file:
        writer = csv.writer(file,delimiter=',')
        writer.writerow(new_student)
    print("Data updated successfully!")

except FileNotFoundError:
    print(f"error: file {file_path} not found!")