import tkinter as tk
from tkinter import ttk, messagebox
from database import create_connection, execute_query
from student_registration import StudentRegistrationForm
from admin_registration import AdminRegistrationForm
from student_dashboard import StudentDashboard
from admin_dashboard import AdminDashboard

class ComplaintManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Complaint Management System")
        self.root.geometry("400x400")
        self.conn = create_connection()

        # Custom colors and fonts
        self.bg_color = "#2c3e50"
        self.fg_color = "#ecf0f1"
        self.button_bg = "#3498db"
        self.button_fg = "#ffffff"
        self.font_style = ("Helvetica", 14)
        self.title_font = ("Helvetica", 18, "bold")

        self.root.configure(bg=self.bg_color)
        self.create_widgets()
    
    def create_widgets(self):
        self.title_label = tk.Label(self.root, text="Welcome to Student Complaint Management System", 
                                  font=self.title_font, bg=self.bg_color, fg="lightgreen")
        self.title_label.pack(pady=(20, 10))

        self.username_label = tk.Label(self.root, text="Username:", font=self.font_style, 
                                     bg=self.bg_color, fg=self.fg_color)
        self.username_label.pack(pady=(10, 0))
        self.username_entry = tk.Entry(self.root, font=self.font_style, width=25, 
                                     bg=self.fg_color, fg="#2c3e50", relief=tk.FLAT)
        self.username_entry.pack(pady=5)

        self.password_label = tk.Label(self.root, text="Password:", font=self.font_style, 
                                     bg=self.bg_color, fg=self.fg_color)
        self.password_label.pack()
        self.password_entry = tk.Entry(self.root, font=self.font_style, width=25, 
                                     show="*", bg=self.fg_color, fg="#2c3e50", relief=tk.FLAT)
        self.password_entry.pack(pady=5)

        self.role_label = tk.Label(self.root, text="Role:", font=self.font_style, 
                                  bg=self.bg_color, fg=self.fg_color)
        self.role_label.pack()
        self.role_combobox = ttk.Combobox(self.root, values=["Student", "Admin"], 
                                         font=self.font_style, state="readonly")
        self.role_combobox.pack(pady=5)

        self.button_frame = tk.Frame(self.root, bg=self.bg_color)
        self.button_frame.pack(pady=10)

        self.sign_in_button = tk.Button(self.button_frame, text="Sign In", font=self.font_style, 
                                       bg=self.button_bg, fg=self.button_fg, relief=tk.FLAT, 
                                       padx=10, pady=5, command=self.sign_in)
        self.sign_in_button.grid(row=0, column=0, padx=5)

        self.sign_up_button = tk.Button(self.button_frame, text="Sign Up", font=self.font_style, 
                                       bg=self.button_bg, fg=self.button_fg, relief=tk.FLAT, 
                                       padx=10, pady=5, command=self.sign_up)
        self.sign_up_button.grid(row=0, column=1, padx=5)

        self.clear_button = tk.Button(self.button_frame, text="Clear", font=self.font_style, 
                                    bg="#e74c3c", fg=self.button_fg, relief=tk.FLAT, 
                                    padx=10, pady=5, command=self.clear_fields)
        self.clear_button.grid(row=0, column=2, padx=5)

    def sign_in(self):
        try:
            username = self.username_entry.get()
            password = self.password_entry.get()
            role = self.role_combobox.get()

            if not username or not password or not role:
                raise ValueError("All fields must be filled!")
            
            cursor = self.conn.cursor()
            table = "student" if role == "Student" else "admin"
            query = f"SELECT * FROM {table} WHERE username = ? AND password = ?"
            cursor.execute(query, (username, password))
            user = cursor.fetchone()
            cursor.close()

            if user:
                self.root.destroy()
                if role == "Student":
                    student_id = user[0]
                    first_name = user[4]
                    dashboard_root = tk.Tk()
                    StudentDashboard(dashboard_root, student_id, self.conn, first_name)
                else:
                    admin_id = user[0]
                    first_name = user[4]
                    dashboard_root = tk.Tk()
                    AdminDashboard(dashboard_root, admin_id, self.conn, first_name)
                    
                dashboard_root.mainloop()
            else:
                messagebox.showerror("Error", "Invalid credentials or not registered!")

        except ValueError as ve:
            messagebox.showerror("Input Error", str(ve))
        except pyodbc.Error as e:
            messagebox.showerror("Database Error", f"Authentication failed: {str(e)}")

    def sign_up(self):
        role = self.role_combobox.get()
        if role == "Student":
            self.show_student_registration_form()
        elif role == "Admin":
            self.show_admin_registration_form()
        else:
            messagebox.showerror("Error", "Please select a role!")

    def show_student_registration_form(self):
        self.root.withdraw()
        student_registration_window = tk.Toplevel()
        StudentRegistrationForm(student_registration_window, self, self.conn)

    def show_admin_registration_form(self):
        self.root.withdraw()
        admin_registration_window = tk.Toplevel()
        AdminRegistrationForm(admin_registration_window, self, self.conn)

    def clear_fields(self):
        try:
            self.username_entry.delete(0, tk.END)
            self.password_entry.delete(0, tk.END)
            self.role_combobox.set("")
        except Exception as e:
            messagebox.showerror("Error", str(e))