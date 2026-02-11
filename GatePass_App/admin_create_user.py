import tkinter as tk
from tkinter import messagebox
import pyodbc

# ---------------- DATABASE ----------------
def get_connection():
    return pyodbc.connect(
        'DRIVER={SQL Server};'
        'SERVER=ATCHYUT;'
        'DATABASE=GatePassDB;'
        'UID=sa;'
        'PWD=Atchyut@2026#;'   # keep local, do not share
    )

# ---------------- LOGIC ----------------
def create_user():
    name = name_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    phone = phone_entry.get()
    flat = flat_entry.get()
    role = role_var.get()

    if not name or not email or not password or not role:
        messagebox.showerror("Error", "Please fill all required fields")
        return

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO Users (Name, Email, Password, Phone, FlatNumber, Role)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (name, email, password, phone, flat, role))

        conn.commit()
        conn.close()

        messagebox.showinfo("Success", f"{role} created successfully")
        clear_fields()

    except Exception as e:
        messagebox.showerror("Database Error", str(e))

def clear_fields():
    name_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)
    password_entry.delete(0, tk.END)
    phone_entry.delete(0, tk.END)
    flat_entry.delete(0, tk.END)
    role_var.set("RESIDENT")

# ---------------- UI OPEN FUNCTION ----------------
def open_create_user_window(parent):
    global window
    global name_entry, email_entry, password_entry, phone_entry, flat_entry, role_var

    window = tk.Toplevel(parent)
    window.title("Admin - Create User")
    window.geometry("400x450")
    window.transient(parent)   # stay on top of dashboard
    window.grab_set()          # block dashboard until closed

    tk.Label(window, text="Create User", font=("Arial", 16)).pack(pady=10)

    tk.Label(window, text="Name").pack()
    name_entry = tk.Entry(window, width=30)
    name_entry.pack()

    tk.Label(window, text="Email").pack()
    email_entry = tk.Entry(window, width=30)
    email_entry.pack()

    tk.Label(window, text="Password").pack()
    password_entry = tk.Entry(window, show="*", width=30)
    password_entry.pack()

    tk.Label(window, text="Phone").pack()
    phone_entry = tk.Entry(window, width=30)
    phone_entry.pack()

    tk.Label(window, text="Flat Number").pack()
    flat_entry = tk.Entry(window, width=30)
    flat_entry.pack()

    tk.Label(window, text="Role").pack()
    role_var = tk.StringVar(value="RESIDENT")
    tk.OptionMenu(window, role_var, "RESIDENT", "SECURITY").pack()

    tk.Button(window, text="Create User", width=20, command=create_user).pack(pady=15)
    tk.Button(window, text="Back", width=15, command=window.destroy).pack(pady=5)
