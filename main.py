import tkinter as tk
from tkinter import messagebox
import datetime

import employee
import attendance
import salary
import payslip_generator
import shutil



# ---------------- MAIN WINDOW ----------------
root = tk.Tk()
root.title("Automated Payroll System")
root.geometry("500x450")
root.resizable(False, False)


# ---------------- HEADER ----------------
header = tk.Label(
    root,
    text="AUTOMATED PAYROLL SYSTEM",
    font=("Helvetica", 18, "bold"),
    fg="white",
    bg="#2c3e50",
    pady=15
)
header.pack(fill="x")


# ---------------- EMPLOYEE MANAGEMENT ----------------

def employee_management():
    win = tk.Toplevel(root)
    win.title("Employee Management")
    win.geometry("420x520")

    tk.Label(win, text="Employee Management",
             font=("Arial", 14, "bold")).pack(pady=10)

    # ------------------ INPUT FIELDS ------------------ #

    tk.Label(win, text="Employee ID").pack()
    e_id_entry = tk.Entry(win)
    e_id_entry.pack()

    tk.Label(win, text="Name").pack()
    name_entry = tk.Entry(win)
    name_entry.pack()

    tk.Label(win, text="Base Salary").pack()
    salary_entry = tk.Entry(win)
    salary_entry.pack()

    # ------------------ FUNCTIONS ------------------ #

    def add_emp():
        try:
            emp_id = e_id_entry.get().strip()
            name = name_entry.get().strip()
            salary = float(salary_entry.get())

            if not emp_id or not name:
                messagebox.showerror("Error", "ID and Name required")
                return

            employee.add_employee(emp_id, name, salary)
            messagebox.showinfo("Success", "Employee added")

            clear_fields()

        except ValueError:
            messagebox.showerror("Error", "Salary must be a number")

    def view_emp():
        employees = employee.get_all_employees()

        if not employees:
            messagebox.showinfo("Employees", "No employees found")
            return

        preview = tk.Toplevel(win)
        preview.title("Employee List")
        preview.geometry("500x400")

        text = tk.Text(preview, wrap=tk.WORD)
        text.pack(expand=True, fill="both")

        for emp in employees:
            text.insert(
                tk.END,
                f"ID: {emp['id']}\n"
                f"Name: {emp['name']}\n"
                f"Base Salary: Rs. {emp['base_salary']}\n"
                "-----------------------------\n"
            )

        text.config(state=tk.DISABLED)

    def search_emp():
        emp_id = e_id_entry.get().strip()
        emp = employee.get_employee_by_id(emp_id)

        if emp:
            name_entry.delete(0, tk.END)
            salary_entry.delete(0, tk.END)

            name_entry.insert(0, emp["name"])
            salary_entry.insert(0, emp["base_salary"])
        else:
            messagebox.showerror("Error", "Employee not found")

    def update_emp():
        try:
            emp_id = e_id_entry.get().strip()
            name = name_entry.get().strip()
            salary = float(salary_entry.get())

            employee.update_employee(emp_id, name, salary)
            messagebox.showinfo("Updated", "Employee updated")
            clear_fields()

        except ValueError:
            messagebox.showerror("Error", "Salary must be numeric")

    def delete_emp():
        emp_id = e_id_entry.get().strip()
        if not emp_id:
            messagebox.showerror("Error", "Enter Employee ID")
            return

        employee.delete_employee(emp_id)
        messagebox.showinfo("Deleted", "Employee deleted")
        clear_fields()

    def clear_fields():
        e_id_entry.delete(0, tk.END)
        name_entry.delete(0, tk.END)
        salary_entry.delete(0, tk.END)

    # ------------------ BUTTONS ------------------ #

    tk.Button(win, text="Add Employee", width=25, command=add_emp).pack(pady=3)
    tk.Button(win, text="View All Employees", width=25, command=view_emp).pack(pady=3)
    tk.Button(win, text="Search by ID", width=25, command=search_emp).pack(pady=3)
    tk.Button(win, text="Update Employee", width=25, command=update_emp).pack(pady=3)
    tk.Button(win, text="Delete Employee", width=25, command=delete_emp).pack(pady=3)

    
# ---------------- ATTENDANCE TRACKING ----------------
import re

def attendance_tracking():
    win = tk.Toplevel(root)
    win.title("Attendance Tracking")
    win.geometry("420x450")

    tk.Label(win, text="Attendance Tracking",
             font=("Arial", 14, "bold")).pack(pady=10)

    # ---------------- INPUT FIELDS ---------------- #

    tk.Label(win, text="Employee ID").pack()
    e_id_entry = tk.Entry(win)
    e_id_entry.pack()

    tk.Label(win, text="Date (YYYY-MM-DD)").pack()
    date_entry = tk.Entry(win)
    date_entry.pack()

    tk.Label(win, text="Status").pack()
    status_var = tk.StringVar(value="Present")
    tk.OptionMenu(win, status_var, "Present", "Absent").pack()

    # ---------------- FUNCTIONS ---------------- #

    def mark_att():
        e_id = e_id_entry.get().strip()
        date = date_entry.get().strip()
        status = status_var.get()

        if not e_id or not date:
            messagebox.showerror("Error", "Employee ID and Date are required")
            return

        # Date format validation
        if not re.match(r"\d{4}-\d{2}-\d{2}", date):
            messagebox.showerror("Error", "Date must be YYYY-MM-DD")
            return

        attendance.mark_attendance(e_id, date, status)
        messagebox.showinfo("Success", "Attendance marked successfully")

    def view_monthly_att():
        e_id = e_id_entry.get().strip()
        date = date_entry.get().strip()

        if not e_id or len(date) < 7:
            messagebox.showerror("Error", "Enter Employee ID and Date")
            return

        month = date[:7]
        count = attendance.get_attendance_for_month(e_id, month)

        messagebox.showinfo(
            "Monthly Attendance",
            f"Employee ID: {e_id}\nMonth: {month}\nDays Present: {count}"
        )

    def view_full_att():
        e_id = e_id_entry.get().strip()
        records = attendance.get_all_attendance(e_id)

        if not records:
            messagebox.showinfo("Attendance", "No attendance records found")
            return

        preview = tk.Toplevel(win)
        preview.title("Attendance Preview")
        preview.geometry("500x400")

        text = tk.Text(preview, wrap=tk.WORD)
        text.pack(expand=True, fill="both")

        text.insert(tk.END, f"Attendance Record for Employee ID: {e_id}\n")
        text.insert(tk.END, "=" * 45 + "\n")

        for date, status in sorted(records.items()):
            text.insert(tk.END, f"{date}  →  {status}\n")

        text.config(state=tk.DISABLED)

    # ---------------- BUTTONS ---------------- #

    tk.Button(win, text="Mark Attendance", width=25,
              command=mark_att).pack(pady=4)

    tk.Button(win, text="View Monthly Attendance", width=25,
              command=view_monthly_att).pack(pady=4)

    tk.Button(win, text="View Full Attendance", width=25,
              command=view_full_att).pack(pady=4)



# ---------------- SALARY CALCULATION ----------------

def salary_calculation():
    win = tk.Toplevel(root)
    win.title("Salary Calculation")
    win.geometry("420x420")

    tk.Label(win, text="Salary Calculation",
             font=("Arial", 14, "bold")).pack(pady=10)

    # ---------------- INPUTS ---------------- #

    tk.Label(win, text="Base Salary").pack()
    salary_entry = tk.Entry(win)
    salary_entry.pack()

    tk.Label(win, text="Days Present (0 - 30)").pack()
    days_entry = tk.Entry(win)
    days_entry.pack()

    # ---------------- FUNCTION ---------------- #

    def calculate():
        try:
            base_salary = float(salary_entry.get())
            days_present = int(days_entry.get())

            result = salary.calculate_salary(base_salary, days_present)

            # ---------- FORMAT OUTPUT ----------
            output = (
                f"Base Salary     : Rs. {result['base_salary']}\n"
                f"Days Present    : {result['days_present']}\n"
                f"Per Day Salary  : Rs. {result['per_day_salary']}\n"
                f"Gross Salary    : Rs. {result['gross_salary']}\n"
                f"Tax Deduction   : Rs. {result['tax_deduction']}\n"
                f"Bonus           : Rs. {result['bonus']}\n"
                f"Net Salary      : Rs. {result['net_salary']}\n"
            )

            # ---------- PREVIEW WINDOW ----------
            preview = tk.Toplevel(win)
            preview.title("Salary Breakdown")
            preview.geometry("450x350")

            tk.Label(preview, text="Salary Breakdown",
                     font=("Arial", 14, "bold")).pack(pady=5)

            text = tk.Text(preview, height=15, width=50)
            text.pack(padx=10, pady=10)

            text.insert(tk.END, output)
            text.config(state=tk.DISABLED)

        except ValueError as e:
            messagebox.showerror("Error", str(e))

    # ---------------- BUTTON ---------------- #

    tk.Button(win, text="Calculate Salary",
              width=25, command=calculate).pack(pady=15)

# ---------------- PAYSLIP GENERATION ----------------
from tkinter import filedialog
import datetime

def show_payslip_preview(emp_data, salary_data):
    preview_win = tk.Toplevel(root)
    preview_win.title("Payslip Preview")
    preview_win.geometry("450x450")
    preview_win.resizable(False, False)

    tk.Label(
        preview_win,
        text="Payslip Preview",
        font=("Arial", 14, "bold")
    ).pack(pady=10)

    payslip_text = f"""
EMPLOYEE PAYSLIP

Company: PayRoll Solutions Pvt. Ltd.
Date: {datetime.datetime.now().strftime('%Y-%m-%d')}

Employee Details:
ID   : {emp_data['id']}
Name : {emp_data['name']}
Role : {emp_data.get('Role', 'Employee')}

Salary Breakdown:
Base Salary  : Rs.{emp_data['Base_Salary']}
Days Present : {salary_data['days_present']}
Gross Pay    : Rs.{salary_data['gross_salary']}
Tax (5%)     : Rs.{salary_data['tax_deduction']}

--------------------------------
Net Pay      : ₹{salary_data['net_salary']}
--------------------------------
"""

    tk.Label(
        preview_win,
        text=payslip_text,
        justify="left",
        font=("Courier", 10),
        anchor="w"
    ).pack(padx=10, pady=10)

    # ---------- BUTTONS ----------
    def download_payslip():
        save_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF Files", "*.pdf")],
            initialfile=f"Payslip_{emp_data['id']}.pdf"
        )

        if save_path:
            generated_file = payslip_generator.generate_payslip(emp_data, salary_data)
            shutil.move(generated_file, save_path)

            messagebox.showinfo(
                "Downloaded",
                f"Payslip saved successfully!\n\n{save_path}"
            )

    def generate_only():
        generated_file = payslip_generator.generate_payslip(emp_data, salary_data)
        messagebox.showinfo("Success", f"Payslip generated in system folder!\n\n{generated_file}")

    tk.Button(
        preview_win,
        text="Download Payslip (PDF)",
        width=25,
        command=download_payslip
    ).pack(pady=5)

    tk.Button(
        preview_win,
        text="Generate Payslip",
        width=25,
        command=generate_only
    ).pack(pady=5)

# ===============================
# EMPLOYEE SEARCH & SALARY LOGIC
# ===============================
def generate_payslip_for_employee(search_key,month):
    emp = None
    search_key = search_key.lower()

    for e in employee.get_all_employees():
        emp_id = str(e.get("id", "")).lower()
        emp_name = str(e.get("name", "")).lower()

        if emp_id == search_key or emp_name == search_key:
            emp = e
            break

    if not emp:
        messagebox.showerror("Not Found", "Employee not found")
        return

    emp_data = {
        "id": str(emp.get("id", "")).strip(),   # must be string
        "name": emp.get("name", "").title(),
        "Role": emp.get("role", "Employee"),
        "Base_Salary": emp.get("base_salary", 0)
    }
    days_present = attendance.get_attendance_for_month(
        emp_data["id"],
        month
    )

    salary_data = salary.calculate_salary(
    base_salary=emp.get("base_salary", 0),
    days_present=days_present
)

    show_payslip_preview(emp_data, salary_data)


# ===============================
# ASK EMPLOYEE + MONTH WINDOW
# ===============================
def ask_employee_for_payslip():
    win = tk.Toplevel(root)
    win.title("Generate Payslip")
    win.geometry("350x250")
    win.resizable(False, False)

    tk.Label(win, text="Generate Payslip", font=("Arial", 14, "bold")).pack(pady=10)

    # Employee
    tk.Label(win, text="Enter Employee ID or Name").pack()
    emp_entry = tk.Entry(win, width=30)
    emp_entry.pack(pady=5)

    # Month
    tk.Label(win, text="Enter Month (YYYY-MM)").pack()
    month_entry = tk.Entry(win, width=30)
    month_entry.pack(pady=5)

    def proceed():
        key = emp_entry.get().strip()
        month = month_entry.get().strip()

        if not key or not month:
            messagebox.showerror(
                "Error",
                "Please enter Employee ID/Name and Month"
            )
            return

        # basic month format check
        if len(month) != 7 or month[4] != "-":
            messagebox.showerror(
                "Invalid Month",
                "Month format should be YYYY-MM (e.g. 2025-01)"
            )
            return

        win.destroy()
        generate_payslip_for_employee(key, month)

    tk.Button(
        win,
        text="Generate Payslip",
        width=20,
        command=proceed
    ).pack(pady=15)



# ---------------- MAIN MENU BUTTONS ----------------
menu_frame = tk.Frame(root, pady=30)
menu_frame.pack()

tk.Button(menu_frame, text="Employee Management", width=30, height=2, command=employee_management).pack(pady=5)
tk.Button(menu_frame, text="Attendance Tracking", width=30, height=2, command=attendance_tracking).pack(pady=5)
tk.Button(menu_frame, text="Calculate Salary", width=30, height=2, command=salary_calculation).pack(pady=5)
tk.Button(menu_frame, text="Generate Payslip", width=30, height=2, command=ask_employee_for_payslip).pack(pady=5)
tk.Button(menu_frame, text="Exit", width=30, height=2, command=root.quit).pack(pady=5)


root.mainloop()
