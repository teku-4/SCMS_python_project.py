import pyodbc
from tkinter import messagebox

def create_connection():
    """Creates and returns a database connection."""
    try:
        conn = pyodbc.connect(
            r'DRIVER={SQL Server};'
            r'SERVER=DESKTOP-7SISEMO\SQLEXPRESS;'
            r'DATABASE=STMS;'
            r'Trusted_Connection=True;'
        )
        print("Database successfully connected")
        conn.autocommit = True
        return conn
    except pyodbc.Error as ex:
        messagebox.showerror("Database Connection Error", f"Could not connect to the database: {ex}")
        return None

def execute_query(conn, query, params=None):
    """Executes a SQL query with optional parameters."""
    if not conn:
        messagebox.showerror("Database Error", "No active database connection")
        return None
    
    try:
        cursor = conn.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        conn.commit()
        return cursor
    except pyodbc.Error as ex:
        messagebox.showerror("Database Query Error", f"Query failed: {ex}")
        return None