import tkinter as tk
from resident_create_visitor import open_create_visitor_window

def open_resident_dashboard(parent):
    window = tk.Toplevel(parent)
    window.title("Resident Dashboard")

    tk.Label(window, text="Resident Dashboard", font=("Arial", 16)).pack(pady=20)

    tk.Button(
        window,
        text="Create Visitor Pass",
        command=lambda: open_create_visitor_window(window)
    ).pack(pady=10)
