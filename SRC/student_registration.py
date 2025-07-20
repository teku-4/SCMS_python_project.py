import tkinter as tk
from tkinter import ttk, messagebox
from database import execute_query

class StudentRegistrationForm:
    def __init__(self, root, main_app, conn):
        self.root = root
        self.main_app = main_app
        self.conn = conn
        self.root.title("Student Registration Form")
        self.root.geometry("500x600")
    
        self.bg_color = "#2c3e50"
        self.fg_color = "#ecf0f1"
        self.button_bg = "#3498db"
        self.button_fg = "#ffffff"
        self.font_style = ("Helvetica", 12)
        self.title_font = ("Helvetica", 16, "bold")

        self.root.configure(bg=self.bg_color)
        self.create_widgets()

    def create_widgets(self):
        self.title_label = tk.Label(self.root, text="Student Registration Form", font=self.title_font,
                                   bg=self.bg_color, fg="lightgreen")
        self.title_label.grid(row=0, column=0, columnspan=2, pady=(20, 10))

        self.student_id_label = tk.Label(self.root, text="Student ID:", font=self.font_style,
                                        bg=self.bg_color, fg=self.fg_color)
        self.student_id_label.grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.student_id_entry = tk.Entry(self.root, font=self.font_style, width=25,
                                        bg=self.fg_color, fg="#2c3e50", relief=tk.FLAT)
        self.student_id_entry.grid(row=1, column=1, padx=10, pady=5)

        self.username_label = tk.Label(self.root, text="Username:", font=self.font_style,
                                      bg=self.bg_color, fg=self.fg_color)
        self.username_label.grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.username_entry = tk.Entry(self.root, font=self.font_style, width=25,
                                      bg=self.fg_color, fg="#2c3e50", relief=tk.FLAT)
        self.username_entry.grid(row=2, column=1, padx=10, pady=5)

        self.password_label = tk.Label(self.root, text="Password:", font=self.font_style,
                                      bg=self.bg_color, fg=self.fg_color)
        self.password_label.grid(row=3, column=0, padx=10, pady=5, sticky="e")
        self.password_entry = tk.Entry(self.root, font=self.font_style, width=25,
                                      show="*", bg=self.fg_color, fg="#2c3e50", relief=tk.FLAT)
        self.password_entry.grid(row=3, column=1, padx=10, pady=5)

        self.email_label = tk.Label(self.root, text="Email:", font=self.font_style,
                                    bg=self.bg_color, fg=self.fg_color)
        self.email_label.grid(row=4, column=0, padx=10, pady=5, sticky="e")
        self.email_entry = tk.Entry(self.root, font=self.font_style, width=25,
                                    bg=self.fg_color, fg="#2c3e50", relief=tk.FLAT)
        self.email_entry.grid(row=4, column=1, padx=10, pady=5)

        self.first_name_label = tk.Label(self.root, text="First Name:", font=self.font_style,
                                         bg=self.bg_color, fg=self.fg_color)
        self.first_name_label.grid(row=5, column=0, padx=10, pady=5, sticky="e")
        self.first_name_entry = tk.Entry(self.root, font=self.font_style, width=25,
                                         bg=self.fg_color, fg="#2c3e50", relief=tk.FLAT)
        self.first_name_entry.grid(row=5, column=1, padx=10, pady=5)

        self.last_name_label = tk.Label(self.root, text="Last Name:", font=self.font_style,
                                        bg=self.bg_color, fg=self.fg_color)
        self.last_name_label.grid(row=6, column=0, padx=10, pady=5, sticky="e")
        self.last_name_entry = tk.Entry(self.root, font=self.font_style, width=25,
                                        bg=self.fg_color, fg="#2c3e50", relief=tk.FLAT)
        self.last_name_entry.grid(row=6, column=1, padx=10, pady=5)

        self.age_label = tk.Label(self.root, text="Age:", font=self.font_style,
                                  bg=self.bg_color, fg=self.fg_color)
        self.age_label.grid(row=7, column=0, padx=10, pady=5, sticky="e")
        self.age_spinbox = tk.Spinbox(self.root, from_=1, to=100, font=self.font_style,
                                      bg=self.fg_color, fg="#2c3e50", relief=tk.FLAT)
        self.age_spinbox.grid(row=7, column=1, padx=10, pady=5)

        self.sex_label = tk.Label(self.root, text="Sex:", font=self.font_style,
                                  bg=self.bg_color, fg=self.fg_color)
        self.sex_label.grid(row=8, column=0, padx=10, pady=5, sticky="e")
        self.sex_var = tk.StringVar(value="Male")
        self.male_radio = tk.Radiobutton(self.root, text="Male", variable=self.sex_var,
                                         value="Male", font=self.font_style, bg=self.bg_color,
                                         fg=self.fg_color)
        self.male_radio.grid(row=8, column=1, padx=10, pady=5, sticky="w")
        self.female_radio = tk.Radiobutton(self.root, text="Female", variable=self.sex_var,
                                           value="Female", font=self.font_style, bg=self.bg_color,
                                           fg=self.fg_color)
        self.female_radio.grid(row=8, column=1, padx=10, pady=5, sticky="e")

        self.department_label = tk.Label(self.root, text="Department:", font=self.font_style,
                                         bg=self.bg_color, fg=self.fg_color)
        self.department_label.grid(row=9, column=0, padx=10, pady=5, sticky="e")
        self.department_entry = tk.Entry(self.root, font=self.font_style, width=25,
                                         bg=self.fg_color, fg="#2c3e50", relief=tk.FLAT)
        self.department_entry.grid(row=9, column=1, padx=10, pady=5)

        self.year_label = tk.Label(self.root, text="Year:", font=self.font_style,
                                   bg=self.bg_color, fg=self.fg_color)
        self.year_label.grid(row=10, column=0, padx=10, pady=5, sticky="e")
        self.year_spinbox = tk.Spinbox(self.root, from_=1, to=8, font=self.font_style,
                                       bg=self.fg_color, fg="#2c3e50", relief=tk.FLAT)
        self.year_spinbox.grid(row=10, column=1, padx=10, pady=5)

        self.semester_label = tk.Label(self.root, text="Semester:", font=self.font_style,
                                       bg=self.bg_color, fg=self.fg_color)
        self.semester_label.grid(row=11, column=0, padx=10, pady=5, sticky="e")
        self.semester_spinbox = tk.Spinbox(self.root, from_=1, to=2, font=self.font_style,
                                           bg=self.fg_color, fg="#2c3e50", relief=tk.FLAT)
        self.semester_spinbox.grid(row=11, column=1, padx=10, pady=5)

        self.button_frame = tk.Frame(self.root, bg=self.bg_color)
        self.button_frame.grid(row=12, column=0, columnspan=2, pady=10)

        self.register_button = tk.Button(self.button_frame, text="Register", font=self.font_style,
                                        bg=self.button_bg, fg=self.button_fg, relief=tk.FLAT,
                                        padx=10, pady=5, command=self.register_student)
        self.register_button.grid(row=0, column=0, padx=5)
        self.clear_button = tk.Button(self.button_frame, text="Clear", font=self.font_style,
                                     bg="#e74c3c", fg=self.button_fg, relief=tk.FLAT,
                                     padx=10, pady=5, command=self.clear_fields)
        self.clear_button.grid(row=0, column=1, padx=5)
        self.back_button = tk.Button(self.button_frame, text="Back", font=self.font_style,
                                    bg="#95a5a6", fg=self.button_fg, relief=tk.FLAT,
                                    padx=10, pady=5, command=self.go_back)
        self.back_button.grid(row=0, column=2, padx=5)

    def register_student(self):
        try:
            student_id = self.student_id_entry.get()
            username = self.username_entry.get()
            password = self.password_entry.get()
            email = self.email_entry.get()
            first_name = self.first_name_entry.get()
            last_name = self.last_name_entry.get()
            age = self.age_spinbox.get()
            sex = self.sex_var.get()
            department = self.department_entry.get()
            year = self.year_spinbox.get()
            semester = self.semester_spinbox.get()

            if not all([student_id, username, password, email, first_name, last_name, age, sex, department, year, semester]):
                raise ValueError("All fields are required!")

            query = """
                INSERT INTO student (student_id, username, password, email, first_name, last_name, age, sex, department, year, semester)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            params = (student_id, username, password, email, first_name, last_name, age, sex, department, year, semester)
            cursor = execute_query(self.conn, query, params)
            if cursor:
                messagebox.showinfo("Success", "Student registered successfully!")
                self.clear_fields()
            else:
                messagebox.showerror("Error", "Failed to register student.")
        except ValueError as ve:
            messagebox.showerror("Input Error", str(ve))
        except Exception as e:
            messagebox.showerror("Database Error", f"An error occurred: {str(e)}")

    def clear_fields(self):
        self.student_id_entry.delete(0, tk.END)
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.first_name_entry.delete(0, tk.END)
        self.last_name_entry.delete(0, tk.END)
        self.age_spinbox.delete(0, tk.END)
        self.sex_var.set("Male")
        self.department_entry.delete(0, tk.END)
        self.year_spinbox.delete(0, tk.END)
        self.semester_spinbox.delete(0, tk.END)

    def go_back(self):
        self.root.destroy()
        self.main_app.root.deiconify()