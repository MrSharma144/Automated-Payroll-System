import json
import os
import csv
from datetime import datetime, date

FILE_NAME = "attendance.json"





def load_attendance():
    """Load attendance data from file."""
    if not os.path.exists(FILE_NAME):
        return {}

    try:
        with open(FILE_NAME, "r") as file:
            return json.load(file)
    except json.JSONDecodeError:
        return {}


def save_attendance(data):
    """Save attendance data to file."""
    with open(FILE_NAME, "w") as file:
        json.dump(data, file, indent=4)


def mark_attendance(e_id, date, status):
    """
    Records attendance for a specific employee and date.
    status should be 'Present' or 'Absent'
    Returns: None
    """
    try:
        attendance_date = datetime.strptime(date, "%Y-%m-%d").date()
        if attendance_date > datetime.today().date():
            print("Cannot mark attendance for a future date.")
            return
    except ValueError:
        print("Invalid date format. Use YYYY-MM-DD.")
        return

    data = load_attendance()

    # Create employee record if not exists
    if e_id not in data:
        data[e_id] = {}

    # Normalize status
    status = status.capitalize()

    if status not in ["Present", "Absent"]:
        print("Invalid status. Use Present or Absent.")
        return

    data[e_id][date] = status
    save_attendance(data)
    print("Attendance marked successfully.")


def get_attendance_for_month(e_id, month):
    """
    Calculates total present days for a given month.
    month format: 'YYYY-MM'
    Returns: integer
    """
    try:
        datetime.strptime(month, "%Y-%m")
    except ValueError:
        print("Invalid month format. Use YYYY-MM.")
        return 0
    
    data = load_attendance()

    if e_id not in data:
        return 0

    present_count = 0

    for date, status in data[e_id].items():
        # Example date: 2026-01-15
        if date.startswith(month) and status == "Present":
            present_count += 1

    return present_count


def get_all_attendance(e_id):
    """
    Returns full attendance record for an employee.
    """
    data = load_attendance()
    return data.get(e_id, {})

if __name__ == "__main__":
    # Test marking attendance
    mark_attendance("E001", "2026-01-10", "Present")
    mark_attendance("E001", "2026-01-11", "Absent")
    mark_attendance("E001", "2026-01-12", "Present")

    # Test future date (should fail)
    mark_attendance("E001", "2099-01-01", "Present")

    # Test invalid date
    mark_attendance("E001", "2026-13-01", "Present")

    # Test monthly count
    count = get_attendance_for_month("E001", "2026-01")
    print("Present days in 2026-01:", count)
