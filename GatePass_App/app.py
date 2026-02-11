import tkinter as tk

window = tk.Tk()
window.title("Input Example")
window.geometry("350x200")

label = tk.Label(window, text="Enter your name:")
label.pack(pady=5)

entry = tk.Entry(window)
entry.pack(pady=5)

result = tk.Label(window, text="")
result.pack(pady=10)

def show_name():
    name = entry.get()
    result.config(text=f"Hello, {name} 😊")

button = tk.Button(window, text="Submit", command=show_name)
button.pack()

window.mainloop()
