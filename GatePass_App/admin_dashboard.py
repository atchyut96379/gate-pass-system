import tkinter as tk
from admin_create_user import open_create_user_window

def open_admin_dashboard(parent):
    window = tk.Toplevel(parent)
    window.title("Admin Dashboard")

    tk.Label(window, text="Admin Dashboard", font=("Arial", 16)).pack(pady=20)

    tk.Button(
        window,
        text="Create User",
        command=lambda: open_create_user_window(window)
    ).pack(pady=10)