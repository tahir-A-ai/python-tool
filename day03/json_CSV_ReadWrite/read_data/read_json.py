import json

json_file_path = 'json_CSV_ReadWrite\data\data.json'
try:
    with open (json_file_path, 'r') as file:
        data = json.load(file)   # this load json data and perform serialization.

        # now we can treat the data as python dict, access its values using keys.
        name = data['name']
        role = data['role']
        organisation = data['organisation']

        print(f"Name: {name} \nRole: {role} \nOrganisation: {organisation}")

except FileNotFoundError:
    print(f"error: file {json_file_path} not found!")