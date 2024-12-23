import tkinter as tk
from tkinter import messagebox
import os
import pandas as pd
from PIL import Image, ImageTk  # For resizing the image

# Hardcoded credentials (username:password)
CREDENTIALS = {"agent1": "1001", "agent2": "1002"}

# Hardcoded file paths
RECORDING_LOG_PATH = "/var/spool/asterisk/monitor/recording.log"
SIP_CONF_PATH = "/etc/asterisk/sip.conf"
QUEUES_LOG_PATH = "/var/log/asterisk/queue_log"  # queues.log path for conversion
CALLBACK_NUMBERS_PATH = "/home/osamara/Downloads/callback_numbers.txt"  # Replace with the actual path for callback numbers

# Path to the image file (provide the PNG path)
CALL_CENTER_IMAGE_PATH = "/home/osamara/Downloads/call_center.png"

# Function to authenticate users
def authenticate(username, password):
    return CREDENTIALS.get(username) == password

# Function to open the file in the default system editor
def open_file_in_editor(file_path):
    try:
        # This will open the file in the default editor (gedit, nano, etc.)
        os.system(f"xdg-open {file_path}")  # xdg-open works on most Linux systems to open in default editor
    except Exception as e:
        messagebox.showerror("Error", f"Failed to open file: {file_path}\n{str(e)}")

# Function to convert queues.log to Excel
def convert_queues_log_to_excel():
    def handle_login():
        username = username_entry.get()
        password = password_entry.get()
        if authenticate(username, password):
            login_window.destroy()
            try:
                # Read the queues.log file into a pandas DataFrame
                with open(QUEUES_LOG_PATH, 'r') as file:
                    lines = file.readlines()

                # Parse the lines (you can adjust this part based on the format of the queues.log file)
                data = []
                for line in lines:
                    data.append([line.strip()])  # If each line is considered as one entry, else adjust parsing

                # Convert the data into a pandas DataFrame
                df = pd.DataFrame(data, columns=['Log Entry'])

                # Save it as an Excel file
                excel_path = "/tmp/queues_log.xlsx"  # Temporary path for the Excel file
                df.to_excel(excel_path, index=False)

                # Open the Excel file using the default viewer
                os.system(f"xdg-open {excel_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to convert queues.log to Excel\n{str(e)}")
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")

    # Login window
    login_window = tk.Toplevel()
    login_window.title("Login")

    tk.Label(login_window, text="Username:").grid(row=0, column=0, padx=10, pady=5)
    username_entry = tk.Entry(login_window)
    username_entry.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(login_window, text="Password:").grid(row=1, column=0, padx=10, pady=5)
    password_entry = tk.Entry(login_window, show="*")
    password_entry.grid(row=1, column=1, padx=10, pady=5)

    tk.Button(login_window, text="Login", command=handle_login).grid(row=2, column=0, columnspan=2, pady=10)

# Function to prompt login before accessing a file
def login_and_access_file(file_path):
    def handle_login():
        username = username_entry.get()
        password = password_entry.get()
        if authenticate(username, password):
            login_window.destroy()
            open_file_in_editor(file_path)  # Open the file in the default editor
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")

    # Login window
    login_window = tk.Toplevel()
    login_window.title("Login")

    tk.Label(login_window, text="Username:").grid(row=0, column=0, padx=10, pady=5)
    username_entry = tk.Entry(login_window)
    username_entry.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(login_window, text="Password:").grid(row=1, column=0, padx=10, pady=5)
    password_entry = tk.Entry(login_window, show="*")
    password_entry.grid(row=1, column=1, padx=10, pady=5)

    tk.Button(login_window, text="Login", command=handle_login).grid(row=2, column=0, columnspan=2, pady=10)

# Main application window
def display_main_window():
    # Create the main window
    main_window = tk.Tk()
    main_window.title("Call Center Log Viewer")

    # Make the window scalable
    main_window.geometry("900x700")  # Larger size for scalability
    main_window.grid_columnconfigure(0, weight=1)  # Make column 0 expandable
    main_window.grid_rowconfigure(1, weight=1)     # Make row 1 expandable (for buttons)

    # Resize and display call center image
    try:
        img = Image.open(CALL_CENTER_IMAGE_PATH)
        img = img.resize((500, 300), Image.ANTIALIAS)  # Resize image to be proportional
        img = ImageTk.PhotoImage(img)
        label_image = tk.Label(main_window, image=img)
        label_image.image = img  # Keep a reference to avoid garbage collection
        label_image.grid(row=0, column=0, columnspan=2, pady=10)  # Placing the image in the grid layout
    except Exception as e:
        messagebox.showwarning("Image Error", f"Could not load or resize call center image.\n{str(e)}")

    # Create buttons and arrange them in a grid for better layout
    button_frame = tk.Frame(main_window)
    button_frame.grid(row=1, column=0, padx=20, pady=20)

    tk.Button(button_frame, text="Open recording.log", command=lambda: login_and_access_file(RECORDING_LOG_PATH)).pack(fill="x", padx=10, pady=5)
    tk.Button(button_frame, text="Open sip.conf", command=lambda: login_and_access_file(SIP_CONF_PATH)).pack(fill="x", padx=10, pady=5)
    tk.Button(button_frame, text="Get Callback Number", command=lambda: login_and_access_file(CALLBACK_NUMBERS_PATH)).pack(fill="x", padx=10, pady=5)
    tk.Button(button_frame, text="Convert queues.log to Excel", command=convert_queues_log_to_excel).pack(fill="x", padx=10, pady=5)

    main_window.mainloop()

# Start the application
display_main_window()
