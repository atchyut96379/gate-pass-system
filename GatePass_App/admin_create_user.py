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
@router.post("/admin/create-user")
def create_user(user: UserCreate):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO users (name, email, password, role, phone, flatnumber)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            user.name,
            user.email,
            user.password,
            user.role,
            user.phone,
            user.flat_number
        ))

        conn.commit()
        return {"message": "User created successfully"}

    except Exception as e:
        conn.rollback()
        print("Error:", e)
        raise HTTPException(status_code=500, detail="Error creating user")

    finally:
        cursor.close()
        conn.close()

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
