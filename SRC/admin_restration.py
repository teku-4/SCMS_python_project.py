import tkinter as tk
from tkinter import ttk, messagebox
from database import execute_query

class AdminRegistrationForm:
    def __init__(self, root, main_app, conn):
        self.root = root
        self.main_app = main_app
        self.conn = conn
        self.root.title("Admin Registration")
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
        self.title_label = tk.Label(self.root, text="Admin Registration", font=self.title_font,
                                   bg=self.bg_color, fg=self.fg_color)
        self.title_label.grid(row=0, column=0, columnspan=2, pady=(20, 10))

        self.admin_id_label = tk.Label(self.root, text="Admin ID:", font=self.font_style,
                                       bg=self.bg_color, fg=self.fg_color)
        self.admin_id_label.grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.admin_id_entry = tk.Entry(self.root, font=self.font_style, width=25,
                                       bg=self.fg_color, fg="#2c3e50", relief=tk.FLAT)
        self.admin_id_entry.grid(row=1, column=1, padx=10, pady=5)

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

        self.position_label = tk.Label(self.root, text="Position:", font=self.font_style,
                                       bg=self.bg_color, fg=self.fg_color)
        self.position_label.grid(row=9, column=0, padx=10, pady=5, sticky="e")
        self.position_entry = tk.Entry(self.root, font=self.font_style, width=25,
                                       bg=self.fg_color, fg="#2c3e50", relief=tk.FLAT)
        self.position_entry.grid(row=9, column=1, padx=10, pady=5)

        self.button_frame = tk.Frame(self.root, bg=self.bg_color)
        self.button_frame.grid(row=10, column=0, columnspan=2, pady=10)

        self.register_button = tk.Button(self.button_frame, text="Register", font=self.font_style,
                                        bg=self.button_bg, fg=self.button_fg, relief=tk.FLAT,
                                        padx=10, pady=5, command=self.register_admin)
        self.register_button.grid(row=0, column=0, padx=5)
        self.clear_button = tk.Button(self.button_frame, text="Clear", font=self.font_style,
                                     bg="#e74c3c", fg=self.button_fg, relief=tk.FLAT,
                                     padx=10, pady=5, command=self.clear_fields)
        self.clear_button.grid(row=0, column=1, padx=5)
        self.back_button = tk.Button(self.button_frame, text="Back", font=self.font_style,
                                    bg="#95a5a6", fg=self.button_fg, relief=tk.FLAT,
                                    padx=10, pady=5, command=self.go_back)
        self.back_button.grid(row=0, column=2, padx=5)

    def register_admin(self):
        try:
            admin_id = self.admin_id_entry.get()
            username = self.username_entry.get()
            password = self.password_entry.get()
            email = self.email_entry.get()
            first_name = self.first_name_entry.get()
            last_name = self.last_name_entry.get()
            age = self.age_spinbox.get()
            sex = self.sex_var.get()
            position = self.position_entry.get()

            if not all([admin_id, username, password, email, first_name, last_name, age, sex, position]):
                raise ValueError("All fields are required!")

            query = """
                INSERT INTO admin (admin_id, username, password, email, first_name, last_name, age, sex, position)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            params = (admin_id, username, password, email, first_name, last_name, age, sex, position)
            cursor = execute_query(self.conn, query, params)
            if cursor:
                messagebox.showinfo("Success", "Admin registered successfully!")
                self.clear_fields()
            else:
                messagebox.showerror("Error", "Failed to register admin.")
        except ValueError as ve:
            messagebox.showerror("Input Error", str(ve))
        except Exception as e:
            messagebox.showerror("Database Error", f"An error occurred: {str(e)}")

    def clear_fields(self):
        self.admin_id_entry.delete(0, tk.END)
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.first_name_entry.delete(0, tk.END)
        self.last_name_entry.delete(0, tk.END)
        self.age_spinbox.delete(0, tk.END)
        self.sex_var.set("Male")
        self.position_entry.delete(0, tk.END)

    def go_back(self):
        self.root.destroy()
        self.main_app.root.deiconify()