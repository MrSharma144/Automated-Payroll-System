import tkinter as tk
from tkinter import ttk, messagebox
import employee
import attendance
import salary
import payslip_generator
import os


# Ensure data directory exists
if not os.path.exists("data"):
    os.makedirs("data")


class PayrollApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Employee Payroll System")
        self.root.geometry("900x600")
        self.root.configure(bg="#ECF0F1")

        # Colors
        self.bg_color = "#ECF0F1"
        self.sidebar_color = "#2C3E50"
        self.header_color = "#34495E"
        self.btn_hover = "#3498DB"
        self.text_color = "white"

        # Layout
        self.main_container = tk.Frame(self.root, bg=self.bg_color)
        self.main_container.pack(fill="both", expand=True)

        self.sidebar = tk.Frame(self.main_container, bg=self.sidebar_color, width=200)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        self.content_area = tk.Frame(self.main_container, bg=self.bg_color)
        self.content_area.pack(side="right", fill="both", expand=True)

        tk.Label(self.sidebar, text="PAYROLL SYS", bg=self.sidebar_color,
                 fg="#1ABC9C", font=("Helvetica", 16, "bold"), pady=20).pack(fill="x")

        self.create_nav_button("Add Employee", self.show_add_employee)
        self.create_nav_button("Mark Attendance", self.show_mark_attendance)
        self.create_nav_button("View Employees", self.show_view_employees)
        self.create_nav_button("Generate Payslip", self.show_generate_payslip)
        self.create_nav_button("Exit", self.root.quit)

        self.show_add_employee()

    # ---------------- COMMON ----------------

    def create_nav_button(self, text, command):
        btn = tk.Button(self.sidebar, text=text, bg=self.sidebar_color,
                        fg=self.text_color, font=("Helvetica", 12),
                        bd=0, activebackground=self.btn_hover,
                        activeforeground="white", command=command, pady=10)
        btn.pack(fill="x", pady=2)

    def clear_content(self):
        for widget in self.content_area.winfo_children():
            widget.destroy()

    def create_label_entry(self, parent, text, row):
        tk.Label(parent, text=text, bg=self.bg_color,
                 font=("Helvetica", 12)).grid(row=row, column=0, padx=10, pady=10, sticky="e")
        entry = tk.Entry(parent, font=("Helvetica", 12), width=30)
        entry.grid(row=row, column=1, padx=10, pady=10)
        self.last_entry = entry

    # ---------------- ADD EMPLOYEE ----------------

    def show_add_employee(self):
        self.clear_content()

        header = tk.Label(self.content_area, text="Add New Employee",
                          bg=self.header_color, fg="white",
                          font=("Helvetica", 16), pady=10)
        header.pack(fill="x")

        form_frame = tk.Frame(self.content_area, bg=self.bg_color, pady=20)
        form_frame.pack()

        self.create_label_entry(form_frame, "Employee ID:", 0)
        self.entry_emp_id = self.last_entry

        self.create_label_entry(form_frame, "Name:", 1)
        self.entry_name = self.last_entry

        self.create_label_entry(form_frame, "Base Salary:", 2)
        self.entry_salary = self.last_entry

        submit_btn = tk.Button(form_frame, text="Add Employee",
                               bg="#27AE60", fg="white",
                               font=("Helvetica", 12, "bold"),
                               padx=20, pady=10,
                               command=self.add_employee_action)
        submit_btn.grid(row=3, column=0, columnspan=2, pady=20)

    def add_employee_action(self):
        try:
            employee.add_employee(
                self.entry_emp_id.get(),
                self.entry_name.get(),
                float(self.entry_salary.get())
            )
            messagebox.showinfo("Success", "Employee added successfully!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # ---------------- ATTENDANCE ----------------

    def show_mark_attendance(self):
        self.clear_content()

        header = tk.Label(self.content_area, text="Mark Attendance",
                          bg=self.header_color, fg="white",
                          font=("Helvetica", 16), pady=10)
        header.pack(fill="x")

        form_frame = tk.Frame(self.content_area, bg=self.bg_color, pady=20)
        form_frame.pack()

        self.create_label_entry(form_frame, "Employee ID:", 0)
        self.att_emp_id = self.last_entry

        self.create_label_entry(form_frame, "Date (YYYY-MM-DD):", 1)
        self.att_date = self.last_entry

        tk.Label(form_frame, text="Status:", bg=self.bg_color,
                 font=("Helvetica", 12)).grid(row=2, column=0)

        self.att_status = ttk.Combobox(form_frame,
                                       values=["Present", "Absent"],
                                       width=27, state="readonly")
        self.att_status.current(0)
        self.att_status.grid(row=2, column=1)

        submit_btn = tk.Button(form_frame, text="Mark Attendance",
                               bg="#E67E22", fg="white",
                               font=("Helvetica", 12, "bold"),
                               padx=20, pady=10,
                               command=self.mark_attendance_action)
        submit_btn.grid(row=3, column=0, columnspan=2, pady=20)

    def mark_attendance_action(self):
        try:
            attendance.mark_attendance(
                self.att_emp_id.get(),
                self.att_date.get(),
                self.att_status.get()
            )
            messagebox.showinfo("Success", "Attendance marked!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # ---------------- VIEW EMPLOYEES ----------------

    def show_view_employees(self):
        self.clear_content()

        header = tk.Label(self.content_area, text="Employee List",
                          bg=self.header_color, fg="white",
                          font=("Helvetica", 16), pady=10)
        header.pack(fill="x")

        table_frame = tk.Frame(self.content_area, bg=self.bg_color)
        table_frame.pack(fill="both", expand=True, padx=20, pady=20)

        cols = ("ID", "Name", "Base Salary")
        tree = ttk.Treeview(table_frame, columns=cols, show='headings')

        for col in cols:
            tree.heading(col, text=col)
            tree.column(col, width=200)

        tree.pack(fill="both", expand=True)

        for emp in employee.get_all_employees():
            tree.insert("", "end",
                        values=(emp["id"], emp["name"], emp["base_salary"]))

    # ---------------- PAYSLIP ----------------

    def show_generate_payslip(self):
        self.clear_content()

        header = tk.Label(self.content_area, text="Generate Payslip",
                          bg=self.header_color, fg="white",
                          font=("Helvetica", 16), pady=10)
        header.pack(fill="x")

        form_frame = tk.Frame(self.content_area, bg=self.bg_color, pady=20)
        form_frame.pack()

        self.create_label_entry(form_frame, "Employee ID:", 0)
        self.pay_emp_id = self.last_entry

        self.create_label_entry(form_frame, "Month (YYYY-MM):", 1)
        self.pay_month = self.last_entry

        tk.Button(form_frame, text="Generate Payslip",
                  bg="#8E44AD", fg="white",
                  font=("Helvetica", 12, "bold"),
                  padx=20, pady=10,
                  command=self.generate_payslip_action).grid(row=2, column=0, columnspan=2, pady=20)

    def generate_payslip_action(self):
        try:
            emp = employee.get_employee_by_id(self.pay_emp_id.get())

            if not emp:
                messagebox.showerror("Error", "Employee not found")
                return

            days = attendance.get_attendance_for_month(
                self.pay_emp_id.get(),
                self.pay_month.get()
            )

            sal = salary.calculate_salary(emp["base_salary"], days)

            emp_data = {
                "ID": emp["id"],
                "Name": emp["name"],
                "Role": "Employee",
                "Base_Salary": emp["base_salary"]
            }

            salary_data = {
                "days_present": days,
                "gross_pay": sal["gross_salary"],
                "tax": sal["tax_deduction"],
                "net_pay": sal["net_salary"]
            }

            file = payslip_generator.generate_payslip(emp_data, salary_data)

            if messagebox.askyesno("Success", "Payslip generated. View now?"):
                os.startfile(os.path.abspath(file))

        except Exception as e:
            messagebox.showerror("Error", str(e))


if __name__ == "__main__":
    root = tk.Tk()
    app = PayrollApp(root)
    root.mainloop()
"""latest"""