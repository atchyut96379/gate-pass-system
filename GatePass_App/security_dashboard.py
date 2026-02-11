import tkinter as tk
from security_verify_otp import open_verify_window

def open_security_dashboard(parent):
    window = tk.Toplevel(parent)
    window.title("Security Dashboard")

    tk.Label(window, text="Security Dashboard", font=("Arial", 16)).pack(pady=20)

    tk.Button(
        window,
        text="Verify Visitor OTP",
        command=lambda: open_verify_window(window)
    ).pack(pady=10)
