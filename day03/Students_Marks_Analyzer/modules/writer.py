import json

def write_summary(file_path, summary):
    try:
        with open(file_path, "w") as file:
            json.dump(summary, file, indent=4)

        print(f"Summary saved to {file_path}")

    except Exception as e:
        print(f"error occured: {e}")
