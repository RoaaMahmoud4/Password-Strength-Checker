# Password Strength Checker
# This program checks the strength of a password based on various criteria.
# It also allows the user to save their password attempts with timestamps and view previous attempts.
import tkinter as tk
from tkinter import messagebox
import string
from datetime import datetime
import os


def check_password_strength(password):
    issues = []
    score = 0
    if 8 <= len(password) <= 15:
        score += 1
    else:
        issues.append("Password must be between 8 and 15 characters.")
    if any(char.isdigit() for char in password):
        score += 1
    else:
        issues.append("Add at least one number.")
    if any(char.islower() for char in password):
        score += 1
    else:
        issues.append("Add at least one lowercase letter.")
    if any(char.isupper() for char in password):
        score += 1
    else:
        issues.append("Add at least one uppercase letter.")
    if any(char in string.punctuation for char in password):
        score += 1
    else:
        issues.append("Add at least one special character.")
    return score, issues


def on_check():
    password = entry.get()
    score, issues = check_password_strength(password)
    result_text.delete("1.0", tk.END)
    if not password:
        messagebox.showwarning("Warning", "Please enter a password.")
    elif len(issues) == 0:
        result_text.insert(tk.END, " Your password is strong!")
    else:
        result_text.insert(tk.END, " Weak Password:\n")
        for i, issue in enumerate(issues):
            result_text.insert(tk.END, f"{i+1}) {issue}\n")
    # Save the attempt with the current date
    save_attempt(password)

# Function to return color based on password score


def get_color(score):
    if score <= 2:
        return "red"
    elif score == 3 or score == 4:
        return "orange"
    else:
        return "green"

# Function to toggle show/hide password


def toggle_password():
    if show_var.get():
        entry.config(show="")
    else:
        entry.config(show="#")

# Function to update color while typing


def update_color_on_typing(event):
    password = entry.get()
    score, _ = check_password_strength(password)
    color = get_color(score)
    entry.config(fg=color)

# Function to save password attempt with date, score, and issues


def save_attempt(password):
    # Get the current date and time
    current_time = datetime.now().strftime(" DAY: %Y-%m-%d ,TIME: %H:%M:%S")
    # Read the current attempts to determine the next attempt number
    try:
        with open("password_attempts.txt", "r") as file:
            lines = file.readlines()
            last_attempt_number = sum(
                1 for line in lines if line.startswith("Attempt"))
    except FileNotFoundError:
        last_attempt_number = 0
    # Increment the attempt number for the new attempt
    attempt_number = last_attempt_number + 1
    # Prepare the result with attempt number and other details
    result = f"Attempt {attempt_number} | {current_time}\nPassword: {password}\n"
    # Save the result to a file
    with open("password_attempts.txt", "a") as file:
        file.write(result)
    # Update the attempts list
    update_attempts_list()

# Function to update the attempts list from the file


def update_attempts_list():
    attempts_list.delete(0, tk.END)
    try:
        with open("password_attempts.txt", "r") as file:
            attempts = file.readlines()
            for attempt in attempts:
                attempts_list.insert(tk.END, attempt.strip())
    except FileNotFoundError:
        pass

 # Function to clear attempts when closing the window


def clear_attempts():
    if os.path.exists("password_attempts.txt"):
        os.remove("password_attempts.txt")


# Create the main window
root = tk.Tk()
root.title("Password Strength Checker")
root.geometry("400x500")
# Label for password entry
tk.Label(root, text="Enter your password:",
         font=("Comic Sans MS", 14)).pack(pady=10)
entry = tk.Entry(root, width=30, show="#")
entry.pack()
entry.bind("<KeyRelease>", update_color_on_typing)
# Show/Hide checkbox
show_var = tk.BooleanVar()
tk.Checkbutton(root, text="Show Password", variable=show_var,
               command=toggle_password).pack(pady=5)
# Button to check password strength
tk.Button(root, text="Check Strength", command=on_check,
          bg="green", fg="white").pack(pady=10)
# Text area for results
result_text = tk.Text(root, height=8, width=45)
result_text.pack(pady=10)
# Listbox to display previous attempts
attempts_label = tk.Label(
    root, text="Previous Attempts:", font=("Comic Sans MS", 12))
attempts_label.pack(pady=10)
attempts_list = tk.Listbox(root, height=6, width=60)
attempts_list.pack(pady=10)
# Load previous attempts when the program starts
update_attempts_list()


def on_close():
    confirm = messagebox.askyesno(
        "Exit Confirmation", "Are you sure you want to exit?\nAll saved attempts will be deleted.")
    if confirm:
        clear_attempts()
        root.destroy()


root.protocol("WM_DELETE_WINDOW", on_close)
# Start the GUI event loop
root.mainloop()
