import tkinter as tk
from tkinter import messagebox
import pyodbc
import random
from datetime import datetime, timedelta

def get_connection():
    return pyodbc.connect(
        'DRIVER={SQL Server};'
        'SERVER=ATCHYUT;'
        'DATABASE=GatePassDB;'
        'UID=sa;'
        'PWD=Atchyut@2026#;'
    )

def generate_otp():
    return str(random.randint(100000, 999999))

def create_visitor():
    name = name_entry.get()
    phone = phone_entry.get()
    purpose = purpose_entry.get()
    flat = flat_entry.get()

    if name == "" or phone == "" or purpose == "" or flat == "":
        messagebox.showerror("Error", "All fields are required")
        return

    otp = generate_otp()
    expiry = datetime.now() + timedelta(minutes=5)

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO Visitors
            (VisitorName, VisitorPhone, Purpose, FlatNumber, OTP, OTPExpiry, Status, CreatedBy)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (name, phone, purpose, flat, otp, expiry, "CREATED", 2))

        conn.commit()
        conn.close()

        messagebox.showinfo(
            "Visitor Pass Created",
            f"OTP: {otp}\nValid for 5 minutes"
        )
        clear_fields()

    except Exception as e:
        messagebox.showerror("Database Error", str(e))

def clear_fields():
    name_entry.delete(0, tk.END)
    phone_entry.delete(0, tk.END)
    purpose_entry.delete(0, tk.END)
    flat_entry.delete(0, tk.END)

# ---------- UI ----------
window = tk.Toplevel()
window.title("Resident - Create Visitor Pass")
window.geometry("400x400")

tk.Label(window, text="Create Visitor Pass", font=("Arial", 16)).pack(pady=10)

tk.Label(window, text="Visitor Name").pack()
name_entry = tk.Entry(window, width=30)
name_entry.pack()

tk.Label(window, text="Visitor Phone").pack()
phone_entry = tk.Entry(window, width=30)
phone_entry.pack()

tk.Label(window, text="Purpose").pack()
purpose_entry = tk.Entry(window, width=30)
purpose_entry.pack()

tk.Label(window, text="Flat Number").pack()
flat_entry = tk.Entry(window, width=30)
flat_entry.pack()

tk.Button(window, text="Generate Pass", width=20, command=create_visitor).pack(pady=20)

window.mainloop()
