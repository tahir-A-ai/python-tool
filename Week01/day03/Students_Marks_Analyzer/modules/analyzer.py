def calculate_summary(data):
    try:
        marks = [student["marks"] for student in data]

        result = {
            "total_students": len(marks),
            "average_marks": sum(marks) / len(marks),
            "highest_marks": max(marks),
            "lowest_marks": min(marks)
        }

        return result

    except Exception as e:
        print(f"unexpected error: {e}")
