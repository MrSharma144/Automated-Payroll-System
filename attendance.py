import json
import os

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
