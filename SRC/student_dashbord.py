import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from database import execute_query

class StudentDashboard:
    def __init__(self, root, student_id, conn, first_name):
        self.root = root
        self.student_id = student_id
        self.conn = conn
        self.root.title(f"Student Dashboard - {first_name}")
        self.root.geometry("1200x800")
        
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('TButton', font=('Helvetica', 12), padding=10)
        self.style.configure('Treeview', rowheight=25)
        
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        nav_frame = ttk.Frame(main_frame, width=200, style='Nav.TFrame')
        nav_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        btn_style = {'style': 'TButton', 'width': 15}
        ttk.Button(nav_frame, text="Submit Complaint", 
                  command=self.show_submit_form, **btn_style).pack(pady=10)
        ttk.Button(nav_frame, text="View Complaints", 
                  command=self.load_complaints, **btn_style).pack(pady=10)
        ttk.Button(nav_frame, text="Log Out", 
                  command=self.logout, **btn_style).pack(pady=10)

        self.tree = ttk.Treeview(main_frame, columns=(
            'ID', 'Title', 'Category', 'Status', 'Date', 'Priority', 'Resolution'
        ), show='headings')
        
        columns = [
            ('ID', 'Complaint ID', 100),
            ('Title', 'Title', 100),
            ('Category', 'Category', 100),
            ('Status', 'Status', 100),
            ('Date', 'Submission Date', 150),
            ('Priority', 'Priority', 100),
            ('Resolution', 'Resolution', 150)
        ]
        
        for col, heading, width in columns:
            self.tree.heading(col, text=heading)
            self.tree.column(col, width=width, anchor=tk.W)

        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.load_complaints()

    def load_complaints(self):
        self.tree.delete(*self.tree.get_children())
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT complaint_id, title, category, status,
                    submission_date, priority, resolution_details
                FROM Complaints
                WHERE student_id = ?
            """, (self.student_id,))
            
            for row in cursor.fetchall():
                priority_map = {1: 'High', 2: 'Medium', 3: 'Low'}
                formatted_row = list(row)
                formatted_row[5] = priority_map.get(formatted_row[5], 'Unknown')
                formatted_row[6] = formatted_row[6] or ''
                formatted_row[4] = row[4].strftime("%Y-%m-%d %H:%M")
                self.tree.insert('', tk.END, values=formatted_row)
                
            cursor.close()
        except pyodbc.Error as e:
            messagebox.showerror("Error", f"Failed to load complaints: {str(e)}")

    def show_submit_form(self):
        self.submit_window = tk.Toplevel(self.root)
        self.submit_window.title("Submit New Complaint")
        self.submit_window.geometry("600x400")
        self.submit_window.configure(bg="#4287f5")

        form_frame = ttk.Frame(self.submit_window)
        form_frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

        ttk.Label(form_frame, text="Title:", font=('Helvetica', 12)).grid(row=0, column=0, sticky='w', pady=5)
        self.title_entry = ttk.Entry(form_frame, width=50)
        self.title_entry.grid(row=0, column=1, pady=5, padx=10)

        ttk.Label(form_frame, text="Category:", font=('Helvetica', 12)).grid(row=1, column=0, sticky='w', pady=5)
        self.category_combo = ttk.Combobox(form_frame, values=[
            'Academic', 'Hostel', 'Financial', 'Infrastructure',
            'Faculty', 'Administrative', 'Other'
        ], state='readonly')
        self.category_combo.grid(row=1, column=1, pady=5, padx=10)

        ttk.Label(form_frame, text="Description:", font=('Helvetica', 12)).grid(row=2, column=0, sticky='nw', pady=5)
        self.desc_text = scrolledtext.ScrolledText(form_frame, width=50, height=10, wrap=tk.WORD)
        self.desc_text.grid(row=2, column=1, pady=5, padx=10)

        submit_btn = ttk.Button(form_frame, text="Submit Complaint", 
                              command=self.save_complaint,
                              style="Submit.TButton")
        submit_btn.grid(row=3, column=1, pady=15, sticky='e')

    def save_complaint(self):
        title = self.title_entry.get().strip()
        category = self.category_combo.get()
        description = self.desc_text.get("1.0", tk.END).strip()

        if not title or not category or not description:
            messagebox.showerror("Error", "All fields are required!")
            return

        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                INSERT INTO Complaints (
                    student_id, title, description, category,
                    submission_date, status, priority
                ) VALUES (?, ?, ?, ?, GETDATE(), 'Open', 3)
            """, (self.student_id, title, description, category))
            
            self.conn.commit()
            messagebox.showinfo("Success", "Complaint submitted successfully!")
            self.submit_window.destroy()
            self.load_complaints()
            
        except pyodbc.Error as e:
            messagebox.showerror("Database Error", f"Failed to submit complaint: {str(e)}")
        finally:
            cursor.close()

    def logout(self):
        from complaint_management import ComplaintManagementApp
        self.root.destroy()
        login_root = tk.Tk()
        ComplaintManagementApp(login_root)
        login_root.mainloop()