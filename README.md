# Automated Payroll System

## Project Overview
The **Automated Payroll System** is a Python-based application designed to streamline the process of managing employee salaries, attendance, and record-keeping for an organization. This system eliminates manual calculation errors and provides a unified interface for HR tasks.

### Key Features
- **Employee Management**: meaningful storage and retrieval of employee details (ID, Name, Base Salary).
- **Attendance Tracking**: System to mark daily attendance and calculate total present days for any given month.
- **Salary Calculation**: Automatic computation of net salary based on base pay and actual days present.
- **Payslip Generation**: Generation of official payslips (e.g., PDF format) for employees.
- **Centralized Interface**: A command-line menu (CLI) that integrates all modules into a seamless user experience.

---

## Student Contributions & Modules
This project was developed collaboratively, with each student responsible for a specific core module.

### 1. Team Lead & Main Interface
**Responsible for:** `main.py` & System Integration
- **Work Description**: 
    - Designed the main architecture of the application.
    - Implemented the Command Line Interface (CLI) menu system.
    - Handled the integration of all other modules (Employee, Attendance, Salary, Payslip).
    - Managed input validation and error handling for the main application loop.
    - Served as the central point of coordination for the project.

### 2. Employee Management Module
**Responsible for:** `employee.py`
- **Work Description**:
    - Created the database/storage logic for employee records.
    - Implemented functions to `add_employee` (saving details like ID, Name, Salary).
    - Developed the `get_all_employees` and `get_employee_by_id` functions to retrieve data.
    - Ensured that employee IDs are unique and data is stored correctly.

### 3. Attendance Tracking Module
**Responsible for:** `attendance.py`
- **Work Description**:
    - Developed the logic to track employee attendance.
    - Implemented `mark_attendance` to record daily status (Present/Absent).
    - Created `get_attendance_for_month` to aggregate attendance data for salary calculations.
    - Managed date formatting and storage of attendance logs.

### 4. Salary Calculation Module
**Responsible for:** `salary.py`
- **Work Description**:
    - Implemented the core financial logic of the system.
    - Created the `calculate_salary` function which takes base salary and attendance data to compute the final payable amount.
    - (Future scope) logic for tax deductions, bonuses, and allowances.

### 5. Payslip Generation Module
**Responsible for:** `payslip_generator.py`
- **Work Description**:
    - Designed the output format for the employee payslips.
    - Implemented `generate_pdf` to create downloadable/viewable payslip documents.
    - Formatted the final output to include company header, employee details, and salary breakdown.

---

## How to Run
1. Ensure Python 3.x is installed.
2. Navigate to the project directory:
   ```bash
   cd Automated-Payroll-System
   ```
3. Run the main application:
   ```bash
   python main.py
   ```
4. Follow the on-screen menu instructions to manage employees and generate payrolls.
