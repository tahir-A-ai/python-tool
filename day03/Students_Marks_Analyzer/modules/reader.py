import csv

def read_csv(file_path):
    try:
        data = []
        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                row['marks'] = int(row['marks'])
                data.append(row)
        return data

    except FileNotFoundError:
        print(f"error: file {file_path} not found")
