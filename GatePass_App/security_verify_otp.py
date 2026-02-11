import tkinter as tk
from tkinter import messagebox
import pyodbc
from datetime import datetime

SECURITY_USER_ID = 3  # example security user id

def get_connection():
    return pyodbc.connect(
        'DRIVER={SQL Server};'
        'SERVER=ATCHYUT;'
        'DATABASE=GatePassDB;'
        'UID=sa;'
        'PWD=Atchyut@2026#;'
    )

def verify_otp():
    flat = flat_entry.get()
    otp = otp_entry.get()

    if flat == "" or otp == "":
        messagebox.showerror("Error", "Enter Flat Number and OTP")
        return

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT VisitorId, OTPExpiry, Status
            FROM Visitors
            WHERE FlatNumber=? AND OTP=?
        """, (flat, otp))

        visitor = cursor.fetchone()

        if not visitor:
            messagebox.showerror("Denied", "Invalid OTP or Flat Number")
            conn.close()
            return

        visitor_id, expiry, status = visitor

        if status != "CREATED":
            messagebox.showerror("Denied", "OTP already used or invalid")
            conn.close()
            return

        if datetime.now() > expiry:
            cursor.execute(
                "UPDATE Visitors SET Status='EXPIRED' WHERE VisitorId=?",
                visitor_id
            )
            conn.commit()
            conn.close()
            messagebox.showerror("Denied", "OTP Expired")
            return

        # APPROVE ENTRY
        cursor.execute(
            "UPDATE Visitors SET Status='APPROVED' WHERE VisitorId=?",
            visitor_id
        )

        cursor.execute("""
            INSERT INTO EntryLogs (VisitorId, VerifiedBy, Status)
            VALUES (?, ?, ?)
        """, (visitor_id, SECURITY_USER_ID, "APPROVED"))

        conn.commit()
        conn.close()

        messagebox.showinfo("Approved", "Visitor Entry Approved")
        clear_fields()

    except Exception as e:
        messagebox.showerror("Database Error", str(e))

def clear_fields():
    flat_entry.delete(0, tk.END)
    otp_entry.delete(0, tk.END)

# ---------- UI ----------
window = tk.Toplevel()
window.title("Security - Verify Visitor")
window.geometry("350x300")

tk.Label(window, text="Verify Visitor OTP", font=("Arial", 16)).pack(pady=10)

tk.Label(window, text="Flat Number").pack()
flat_entry = tk.Entry(window, width=30)
flat_entry.pack()

tk.Label(window, text="OTP").pack()
otp_entry = tk.Entry(window, width=30)
otp_entry.pack()

tk.Button(window, text="Verify Entry", width=20, command=verify_otp).pack(pady=20)

window.mainloop()
