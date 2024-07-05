import tkinter as tk
from tkinter import filedialog, messagebox, Checkbutton, IntVar
import re
import os

def browse_file():
    filename = filedialog.askopenfilename(filetypes=[("Python files", "*.py")])
    if filename:
        file_path.set(filename)

def generate_output():
    if not file_path.get():
        messagebox.showwarning("Warning", "Please select a Python file.")
        return
    
    packages = set()
    with open(file_path.get(), 'r') as file:
        for line in file:
            matches = re.findall(r'^\s*(?:import|from)\s+([a-zA-Z0-9_]+)', line)
            packages.update(matches)
    
    if install_var.get():
        file_dir = os.path.dirname(file_path.get())
        batch_file_path = os.path.join(file_dir, 'install_packages.bat')
        with open(batch_file_path, 'w') as bat_file:
            bat_file.write("@echo off\n")
            for package in packages:
                bat_file.write(f"pip install {package}\n")
        messagebox.showinfo("Success", f"Batch file 'install_packages.bat' generated successfully in {file_dir}!")
    else:
        package_list = '\n'.join(packages)
        messagebox.showinfo("Required Packages", f"The following packages are required:\n\n{package_list}")

def center_window(app, width=400, height=200):
    # Get screen width and height
    screen_width = app.winfo_screenwidth()
    screen_height = app.winfo_screenheight()
    
    # Calculate position x and y coordinates
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    
    app.geometry(f'{width}x{height}+{x}+{y}')

app = tk.Tk()
app.title("Python Package Scanner")

# Center the main window
center_window(app)

file_path = tk.StringVar()
install_var = IntVar()

frame = tk.Frame(app)
frame.pack(pady=20, padx=20)

file_label = tk.Label(frame, text="Python File:")
file_label.grid(row=0, column=0, padx=5, pady=5)

file_entry = tk.Entry(frame, textvariable=file_path, width=40)
file_entry.grid(row=0, column=1, padx=5, pady=5)

browse_button = tk.Button(frame, text="Browse", command=browse_file)
browse_button.grid(row=0, column=2, padx=5, pady=5)

install_checkbox = Checkbutton(frame, text="Generate .bat File", variable=install_var)
install_checkbox.grid(row=1, columnspan=3, padx=5, pady=5)

generate_button = tk.Button(frame, text="Start", command=generate_output)
generate_button.grid(row=2, columnspan=3, padx=5, pady=10)

app.mainloop()
