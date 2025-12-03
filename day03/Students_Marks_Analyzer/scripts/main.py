from modules.reader import read_csv
from modules.analyzer import calculate_summary
from modules.writer import write_summary

def main():
    try:
        input_file = "../data/student.csv"
        output_file = "../data/summary.json"

        data = read_csv(input_file)
        summary = calculate_summary(data)
        write_summary(output_file, summary)

        print("\nStudent Marks Summary:")
        print(summary)

    except Exception as e:
        print(f"Error in main program: {e}")

if __name__ == "__main__":
    main()
