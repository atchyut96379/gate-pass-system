import tkinter as tk
from tkinter import messagebox
import pyodbc
import os
# ---------- DATABASE CONNECTION ----------
def get_connection():
    return pyodbc.connect(
        'DRIVER={SQL Server};'
        'SERVER=ATCHYUT;'
        'DATABASE=GatePassDB;'
        'UID=sa;'
        'PWD=Atchyut@2026#;'
    )

# ---------- LOGIN FUNCTION ----------
def login():
    email = email_entry.get()
    password = password_entry.get()

    if email == "" or password == "":
        messagebox.showerror("Error", "Please enter email and password")
        return

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT Name, Role FROM Users WHERE Email=? AND Password=?",
            (email, password)
        )

        user = cursor.fetchone()
        conn.close()

        if user:
            name, role = user
            open_dashboard(name, role)
        else:
            messagebox.showerror("Login Failed", "Invalid email or password")

    except Exception as e:
        messagebox.showerror("Database Error", str(e))

# ---------- DASHBOARDS ----------
def open_dashboard(name, role):
    # Hide login window but keep Tk alive
    login_window.withdraw()

    if role == "ADMIN":
        from admin_dashboard import open_admin_dashboard
        open_admin_dashboard(login_window)

    elif role == "RESIDENT":
        from resident_dashboard import open_resident_dashboard
        open_resident_dashboard(login_window)

    elif role == "SECURITY":
        from security_dashboard import open_security_dashboard
        open_security_dashboard(login_window)

    else:
        messagebox.showerror("Access Denied", "Invalid role")
        login_window.deiconify()

# ---------- LOGIN UI ----------
login_window = tk.Tk()
login_window.title("GatePassApp - Login")
login_window.geometry("350x250")

tk.Label(login_window, text="Email").pack(pady=5)
email_entry = tk.Entry(login_window, width=30)
email_entry.pack()

tk.Label(login_window, text="Password").pack(pady=5)
password_entry = tk.Entry(login_window, show="*", width=30)
password_entry.pack()

tk.Button(
    login_window,
    text="Login",
    width=15,
    command=login
).pack(pady=20)

login_window.mainloop()
