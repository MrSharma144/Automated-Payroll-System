import json
import os

FILE_NAME = "employees.json"


def load_employees():
    """Load employees from file."""
    if not os.path.exists(FILE_NAME):
        return []
    try:
        with open(FILE_NAME, "r") as file:
            return json.load(file)
    except json.JSONDecodeError:
        return []


def save_employees(data):
    """Save employees to file."""
    with open(FILE_NAME, "w") as file:
        json.dump(data, file, indent=4)


def add_employee(id, name, base_salary):
    """
    Stores employee ID, name, and base salary.
    Returns: None
    """
    employees = load_employees()

    # Optional: prevent duplicate ID
    for emp in employees:
        if emp["id"] == id:
            print("Employee ID already exists.")
            return

    new_employee = {
        "id": id,
        "name": name,
        "base_salary": base_salary
    }

    employees.append(new_employee)
    save_employees(employees)
    print("Employee added successfully.")


def get_all_employees():
    """
    Retrieves all stored employee records.
    Returns: List of employees
    """
    return load_employees()


def get_employee_by_id(id):
    """
    Fetch a single employee using ID.
    Returns: employee dictionary or None if not found
    """
    employees = load_employees()

    for emp in employees:
        if emp["id"] == id:
            return emp

    return None


def delete_employee(id):
    """
    Deletes an employee by ID.
    Returns: None
    """
    employees = load_employees()

    updated_employees = [emp for emp in employees if emp["id"] != id]

    if len(updated_employees) == len(employees):
        print("Employee not found.")
        return

    save_employees(updated_employees)
    print("Employee deleted successfully.")

def update_employee(id, name=None, base_salary=None):
    """
    Updates an employee's details by ID.
    Returns: None
    """
    employees = load_employees()
    found = False

    for emp in employees:
        if emp["id"] == id:
            if name is not None:
                emp["name"] = name
            if base_salary is not None:
                emp["base_salary"] = base_salary
            found = True
            break

    if not found:
        print("Employee not found.")
        return

    save_employees(employees)
    print("Employee updated successfully.")