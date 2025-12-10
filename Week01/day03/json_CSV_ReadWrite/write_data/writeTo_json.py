import json

file_path = 'json_CSV_ReadWrite\data\data.json'

try:
    with open(file_path, 'r') as file:
        data = json.load(file)
    
    # write to th file / modify data
    data['Joining Date'] = '1st December 2025'

    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)
    
    print("Data updated successfully!")

except FileNotFoundError:
    print(f"error: file {file_path} not found!")