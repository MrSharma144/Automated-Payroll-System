import employee
import attendance
import salary
import payslip_generator
import sys

def print_header():
    print("=" * 50)
    print("       AUTOMATED PAYROLL SYSTEM      ")
    print("=" * 50)

def print_menu():
    print("\nMAIN MENU:")
    print("1. Employee Management (Add/View)")
    print("2. Attendance Tracking (Mark/View)")
    print("3. Calculate Salary")
    print("4. Generate Payslip")
    print("5. Exit")

def handle_employee_management():
    print("\n--- Employee Management ---")
    print("1. Add Employee")
    print("2. View All Employees")
    choice = input("Enter choice: ")
    
    if choice == '1':
        try:
            e_id = input("Enter Employee ID: ")
            name = input("Enter Name: ")
            salary_input = input("Enter Base Salary: ")
            base_salary = float(salary_input)
            employee.add_employee(e_id, name, base_salary)
        except ValueError:
            print("Invalid input for salary. Please enter a number.")
    elif choice == '2':
        employees = employee.get_all_employees()
        print("Employees:", employees)
    else:
        print("Invalid choice.")

def handle_attendance_tracking():
    print("\n--- Attendance Tracking ---")
    print("1. Mark Attendance")
    print("2. View Attendance for Month")
    choice = input("Enter choice: ")

    if choice == '1':
        e_id = input("Enter Employee ID: ")
        date = input("Enter Date (YYYY-MM-DD): ")
        status = input("Enter Status (Present/Absent): ")
        attendance.mark_attendance(e_id, date, status)
    elif choice == '2':
        e_id = input("Enter Employee ID: ")
        month = input("Enter Month (YYYY-MM): ")
        count = attendance.get_attendance_for_month(e_id, month)
        print(f"Days present: {count}")
    else:
        print("Invalid choice.")

def handle_salary_calculation():
    print("\n--- Calculate Salary ---")
    try:
        base_salary = float(input("Enter Base Salary: "))
        days_present = int(input("Enter Days Present: "))
        result = salary.calculate_salary(base_salary, days_present)
        print("Salary Breakdown:", result)
    except ValueError:
        print("Invalid input for numbers.")

def handle_payslip_generation():
    print("\n--- Generate Payslip ---")
    # In a real scenario, we would fetch this data first
    print("Note: This is a stub action. Data gathering would happen here.")
    employee_data = {"name": "Test User", "id": "101"}
    salary_data = {"net_salary": 5000} 
    payslip_generator.generate_pdf(employee_data, salary_data)

def main():
    print_header()
    while True:
        print_menu()
        choice = input("Enter your choice (1-5): ")

        if choice == '1':
            handle_employee_management()
        elif choice == '2':
            handle_attendance_tracking()
        elif choice == '3':
            handle_salary_calculation()
        elif choice == '4':
            handle_payslip_generation()
        elif choice == '5':
            print("Exiting system. Goodbye!")
            sys.exit()
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()