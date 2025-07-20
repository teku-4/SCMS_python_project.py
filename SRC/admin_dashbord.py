import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from database import execute_query

class AdminDashboard:
    def __init__(self, root, admin_id, conn, first_name):
        self.root = root
        self.admin_id = admin_id
        self.conn = conn
        self.root.title(f"Admin Dashboard - {first_name}")
        self.root.geometry("1400x800")
        
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('TButton', font=('Helvetica', 12), padding=10)
        self.style.configure('Treeview', rowheight=25, font=('Helvetica', 11))
        self.style.configure('Header.Treeview', font=('Helvetica', 12, 'bold'))
        
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        nav_frame = ttk.Frame(main_frame, width=220, style='Nav.TFrame')
        nav_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        btn_style = {'style': 'TButton', 'width': 18}
        ttk.Button(nav_frame, text="View All Complaints", 
                  command=self.load_all_complaints, **btn_style).pack(pady=12)
        ttk.Button(nav_frame, text="Resolve Complaint", 
                  command=self.resolve_complaint, **btn_style).pack(pady=12)
        ttk.Button(nav_frame, text="Generate Report", 
                  command=self.generate_report, **btn_style).pack(pady=12)
        ttk.Button(nav_frame, text="Manage Complaints", 
                  command=self.manage_complaints, **btn_style).pack(pady=12)
        ttk.Button(nav_frame, text="Log Out", 
                  command=self.logout, **btn_style).pack(pady=12)

        self.tree = ttk.Treeview(main_frame, columns=(
            'ID', 'Title', 'Category', 'Status', 'Date', 'Student', 'Priority', 'Resolution'
        ), show='headings')
        
        columns = [
            ('ID', 'Complaint ID', 50),
            ('Title', 'Title', 150),
            ('Category', 'Category', 100),
            ('Status', 'Status', 100),
            ('Date', 'Submission Date', 150),
            ('Student', 'Student ID', 80),
            ('Priority', 'Priority', 45),
            ('Resolution', 'Resolution', 200)
        ]
        
        for col, heading, width in columns:
            self.tree.heading(col, text=heading)
            self.tree.column(col, width=width, anchor=tk.W)

        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.load_all_complaints()

    def load_all_complaints(self):
        self.tree.delete(*self.tree.get_children())
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT complaint_id, title, category, status,
                    submission_date, student_id, priority, resolution_details
                FROM Complaints
            """)
            
            for row in cursor.fetchall():
                priority_map = {1: 'High', 2: 'Medium', 3: 'Low'}
                formatted_row = list(row)
                formatted_row[6] = priority_map.get(formatted_row[6], 'Unknown')
                formatted_row[7] = formatted_row[7] or ''
                formatted_row[4] = row[4].strftime("%Y-%m-%d %H:%M")
                self.tree.insert('', tk.END, values=formatted_row)
                
            cursor.close()
        except pyodbc.Error as e:
            messagebox.showerror("Error", f"Failed to load complaints: {str(e)}")

    def resolve_complaint(self):
        self.resolve_window = tk.Toplevel(self.root)
        self.resolve_window.title("Resolve Complaint")
        self.resolve_window.geometry("500x400")
        self.resolve_window.configure(bg="#f0f2f5")

        form_frame = ttk.Frame(self.resolve_window)
        form_frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

        ttk.Label(form_frame, text="Complaint ID:", font=('Helvetica', 12)).grid(row=0, column=0, sticky='w', pady=5)
        self.complaint_id_entry = ttk.Entry(form_frame, width=15)
        self.complaint_id_entry.grid(row=0, column=1, pady=5, padx=10, sticky='w')

        ttk.Label(form_frame, text="Resolution Status:", font=('Helvetica', 12)).grid(row=1, column=0, sticky='w', pady=5)
        self.status_combo = ttk.Combobox(form_frame, values=[
            'Resolved', 'Closed', 'Rejected'
        ], state='readonly')
        self.status_combo.grid(row=1, column=1, pady=5, padx=10, sticky='w')

        ttk.Label(form_frame, text="Resolution Details:", font=('Helvetica', 12)).grid(row=2, column=0, sticky='nw', pady=5)
        self.resolution_text = scrolledtext.ScrolledText(form_frame, width=40, height=8, wrap=tk.WORD)
        self.resolution_text.grid(row=2, column=1, pady=5, padx=10)

        resolve_btn = ttk.Button(form_frame, text="Submit Resolution", 
                               command=self.submit_resolution,
                               style="Resolve.TButton")
        resolve_btn.grid(row=3, column=1, pady=15, sticky='e')

    def submit_resolution(self):
        complaint_id = self.complaint_id_entry.get().strip()
        status = self.status_combo.get()
        resolution = self.resolution_text.get("1.0", tk.END).strip()

        if not complaint_id or not status or not resolution:
            messagebox.showerror("Error", "All fields are required!")
            return

        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT complaint_id FROM Complaints WHERE complaint_id = ?", (complaint_id,))
            if not cursor.fetchone():
                messagebox.showerror("Error", "Invalid Complaint ID!")
                return

            cursor.execute("""
                UPDATE Complaints 
                SET resolution_details = ?,
                    status = ?,
                    resolution_date = GETDATE(),
                    admin_id = ?
                WHERE complaint_id = ?
            """, (resolution, status, self.admin_id, complaint_id))
            
            self.conn.commit()
            messagebox.showinfo("Success", "Complaint resolved successfully!")
            self.resolve_window.destroy()
            self.load_all_complaints()
            
        except pyodbc.Error as e:
            messagebox.showerror("Database Error", f"Failed to resolve complaint: {str(e)}")
        finally:
            cursor.close()

    def generate_report(self):
        report_window = tk.Toplevel(self.root)
        report_window.title("Complaint Statistics Report")
        report_window.geometry("800x600")
        report_window.configure(bg="#4287f5")

        main_frame = ttk.Frame(report_window)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        ttk.Label(main_frame, 
                text="Complaint Statistics Report", 
                font=('Helvetica', 16, 'bold')).pack(pady=15)

        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT status, COUNT(*) AS count 
                FROM Complaints 
                GROUP BY status
            """)
            status_data = cursor.fetchall()
            status_dict = {status: count for status, count in status_data}

            cursor.execute("SELECT COUNT(*) FROM Complaints")
            total_complaints = cursor.fetchone()[0]

            cursor.execute("""
                SELECT category, COUNT(*) AS count 
                FROM Complaints 
                GROUP BY category
            """)
            category_data = cursor.fetchall()

            cursor.execute("""
                SELECT priority, COUNT(*) AS count 
                FROM Complaints 
                GROUP BY priority
            """)
            priority_data = cursor.fetchall()

            cursor.close()

        except pyodbc.Error as e:
            messagebox.showerror("Database Error", f"Failed to generate report: {str(e)}")
            return

        status_frame = ttk.LabelFrame(main_frame, text="Status Distribution")
        status_frame.pack(fill=tk.X, pady=10, padx=10)

        predefined_statuses = ['Open', 'In Progress', 'Resolved', 'Closed', 'Rejected']
        for status in predefined_statuses:
            row = ttk.Frame(status_frame)
            row.pack(fill=tk.X, pady=3)
            ttk.Label(row, text=status, width=15, anchor='w').pack(side=tk.LEFT, padx=5)
            ttk.Label(row, text=str(status_dict.get(status, 0))).pack(side=tk.RIGHT, padx=5)

        total_frame = ttk.LabelFrame(main_frame, text="Total Complaints")
        total_frame.pack(fill=tk.X, pady=10, padx=10)
        ttk.Label(total_frame, text=str(total_complaints), font=('Helvetica', 14)).pack(pady=5)

        category_frame = ttk.LabelFrame(main_frame, text="Category Distribution")
        category_frame.pack(fill=tk.BOTH, pady=10, padx=10, expand=True)

        for category, count in category_data:
            row = ttk.Frame(category_frame)
            row.pack(fill=tk.X, pady=3)
            ttk.Label(row, text=category, width=20, anchor='w').pack(side=tk.LEFT, padx=5)
            ttk.Label(row, text=str(count)).pack(side=tk.RIGHT, padx=5)

        priority_frame = ttk.LabelFrame(main_frame, text="Priority Distribution")
        priority_frame.pack(fill=tk.BOTH, pady=10, padx=10, expand=True)

        for priority, count in priority_data:
            row = ttk.Frame(priority_frame)
            row.pack(fill=tk.X, pady=3)
            ttk.Label(row, text=priority, width=15, anchor='w').pack(side=tk.LEFT, padx=5)
            ttk.Label(row, text=str(count)).pack(side=tk.RIGHT, padx=5)

        disclaimer = ttk.Label(main_frame, 
                            text="Note: Historical tracking of deletions and updates requires additional logging.", 
                            font=('Helvetica', 9), 
                            foreground='gray50')
        disclaimer.pack(pady=10)

    def manage_complaints(self):
        self.manage_window = tk.Toplevel(self.root)
        self.manage_window.title("Manage Complaints")
        self.manage_window.geometry("400x250")
        self.manage_window.configure(bg="#4287f5")

        form_frame = ttk.Frame(self.manage_window)
        form_frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

        ttk.Label(form_frame, text="Complaint ID:", font=('Helvetica', 12)).grid(row=0, column=0, sticky='w', pady=10)
        self.manage_complaint_id = ttk.Entry(form_frame, width=15)
        self.manage_complaint_id.grid(row=0, column=1, pady=10, padx=10, sticky='w')

        delete_btn = ttk.Button(form_frame, text="Delete Complaint", 
                              command=self.delete_complaint,
                              style="Danger.TButton")
        delete_btn.grid(row=1, column=1, pady=15, sticky='e')
        update_btn = ttk.Button(form_frame, text="Update Complaint", 
                              command=self.update_complaint,
                              style="Update.TButton")
        update_btn.grid(row=1, column=0, pady=15, sticky='e')

    def delete_complaint(self):
        complaint_id = self.manage_complaint_id.get().strip()
        
        if not complaint_id:
            messagebox.showerror("Error", "Please enter a Complaint ID!")
            return

        confirm = messagebox.askyesno("Confirm Delete", 
                                    "Are you sure you want to delete this complaint?\nThis action cannot be undone!")
        if not confirm:
            return

        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT complaint_id FROM Complaints WHERE complaint_id = ?", (complaint_id,))
            if not cursor.fetchone():
                messagebox.showerror("Error", "Invalid Complaint ID!")
                return

            cursor.execute("DELETE FROM Complaints WHERE complaint_id = ?", (complaint_id,))
            self.conn.commit()
            
            messagebox.showinfo("Success", "Complaint deleted successfully!")
            self.manage_window.destroy()
            self.load_all_complaints()
            
        except pyodbc.Error as e:
            messagebox.showerror("Database Error", f"Failed to delete complaint: {str(e)}")
        finally:
            cursor.close()

    def update_complaint(self):
        self.update_window = tk.Toplevel(self.root)
        self.update_window.title("Update Complaint Details")
        self.update_window.geometry("500x400")
        self.update_window.configure(bg="#4287f5")

        form_frame = ttk.Frame(self.update_window)
        form_frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

        ttk.Label(form_frame, text="Complaint ID:", font=('Helvetica', 12)).grid(row=0, column=0, sticky='w', pady=5)
        self.update_id_entry = ttk.Entry(form_frame, width=15)
        self.update_id_entry.grid(row=0, column=1, pady=5, padx=10, sticky='w')

        ttk.Label(form_frame, text="New Category:", font=('Helvetica', 12)).grid(row=1, column=0, sticky='w', pady=5)
        self.new_category = ttk.Combobox(form_frame, values=[
            'Academic', 'Hostel', 'Financial', 'Infrastructure',
            'Faculty', 'Administrative', 'Other'
        ], state='readonly')
        self.new_category.grid(row=1, column=1, pady=5, padx=10, sticky='w')

        ttk.Label(form_frame, text="New Status:", font=('Helvetica', 12)).grid(row=2, column=0, sticky='w', pady=5)
        self.new_status = ttk.Combobox(form_frame, values=[
            'Open', 'In Progress', 'Resolved', 'Closed', 'Rejected'
        ], state='readonly')
        self.new_status.grid(row=2, column=1, pady=5, padx=10, sticky='w')

        update_btn = ttk.Button(form_frame, text="Update Complaint", 
                              command=self.submit_update,
                              style="Update.TButton")
        update_btn.grid(row=3, column=1, pady=15, sticky='e')

    def submit_update(self):
        complaint_id = self.update_id_entry.get().strip()
        new_category = self.new_category.get()
        new_status = self.new_status.get()

        if not complaint_id:
            messagebox.showerror("Error", "Complaint ID is required!")
            return

        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT complaint_id FROM Complaints WHERE complaint_id = ?", (complaint_id,))
            if not cursor.fetchone():
                messagebox.showerror("Error", "Invalid Complaint ID!")
                return

            update_fields = []
            params = []
            
            if new_category:
                update_fields.append("category = ?")
                params.append(new_category)
            if new_status:
                update_fields.append("status = ?")
                params.append(new_status)

            if not update_fields:
                messagebox.showerror("Error", "No fields to update!")
                return

            params.append(complaint_id)
            query = f"UPDATE Complaints SET {', '.join(update_fields)} WHERE complaint_id = ?"
            
            cursor.execute(query, params)
            self.conn.commit()
            
            messagebox.showinfo("Success", "Complaint updated successfully!")
            self.update_window.destroy()
            self.load_all_complaints()
            
        except pyodbc.Error as e:
            messagebox.showerror("Database Error", f"Failed to update complaint: {str(e)}")
        finally:
            cursor.close()

    def logout(self):
        from complaint_management import ComplaintManagementApp
        self.root.destroy()
        login_root = tk.Tk()
        ComplaintManagementApp(login_root)
        login_root.mainloop()