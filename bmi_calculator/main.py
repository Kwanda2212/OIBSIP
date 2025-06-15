import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
import matplotlib.pyplot as plt
from datetime import datetime

# Database setup
conn = sqlite3.connect("bmi_database.db")
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS bmi_records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    weight REAL,
    height REAL,
    bmi REAL,
    category TEXT,
    date TEXT
)
""")
conn.commit()

# BMI Category Logic
def get_bmi_category(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif 18.5 <= bmi < 25:
        return "Normal"
    elif 25 <= bmi < 30:
        return "Overweight"
    else:
        return "Obese"

# Calculate BMI
def calculate_bmi():
    try:
        username = entry_name.get().strip()
        weight = float(entry_weight.get())
        height = float(entry_height.get())

        if not username:
            raise ValueError("Username is required.")
        if weight <= 0 or height <= 0:
            raise ValueError("Height and weight must be positive numbers.")

        bmi = round(weight / (height ** 2), 2)
        category = get_bmi_category(bmi)
        label_result.config(text=f"BMI: {bmi} ({category})")

        # Save to DB
        cursor.execute("INSERT INTO bmi_records (username, weight, height, bmi, category, date) VALUES (?, ?, ?, ?, ?, ?)",
                       (username, weight, height, bmi, category, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        conn.commit()

        messagebox.showinfo("Success", "BMI recorded successfully.")
    except ValueError as ve:
        messagebox.showerror("Input Error", str(ve))
    except Exception as e:
        messagebox.showerror("Error", f"An unexpected error occurred: {e}")

# View History
def view_history():
    username = entry_name.get().strip()
    if not username:
        messagebox.showwarning("Warning", "Please enter a username to view history.")
        return

    cursor.execute("SELECT date, bmi FROM bmi_records WHERE username = ? ORDER BY date ASC", (username,))
    records = cursor.fetchall()

    if not records:
        messagebox.showinfo("No Data", f"No BMI records found for {username}.")
        return

    dates = [datetime.strptime(r[0], "%Y-%m-%d %H:%M:%S") for r in records]
    bmis = [r[1] for r in records]

    plt.figure(figsize=(8, 5))
    plt.plot(dates, bmis, marker='o')
    plt.title(f"{username}'s BMI Trend")
    plt.xlabel("Date")
    plt.ylabel("BMI")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.grid(True)
    plt.show()

# GUI Setup
app = tk.Tk()
app.title("Advanced BMI Calculator")
app.geometry("400x400")

tk.Label(app, text="Advanced BMI Calculator", font=("Arial", 16)).pack(pady=10)

frame = tk.Frame(app)
frame.pack(pady=10)

tk.Label(frame, text="Username:").grid(row=0, column=0, sticky="e")
entry_name = tk.Entry(frame, width=25)
entry_name.grid(row=0, column=1)

tk.Label(frame, text="Weight (kg):").grid(row=1, column=0, sticky="e")
entry_weight = tk.Entry(frame, width=25)
entry_weight.grid(row=1, column=1)

tk.Label(frame, text="Height (m):").grid(row=2, column=0, sticky="e")
entry_height = tk.Entry(frame, width=25)
entry_height.grid(row=2, column=1)

label_result = tk.Label(app, text="", font=("Arial", 12))
label_result.pack(pady=10)

tk.Button(app, text="Calculate BMI", command=calculate_bmi, bg="#4CAF50", fg="white", width=20).pack(pady=5)
tk.Button(app, text="View History", command=view_history, bg="#2196F3", fg="white", width=20).pack(pady=5)

tk.Label(app, text="(c) 2025 BMI Tracker App", font=("Arial", 8)).pack(side="bottom", pady=10)

app.mainloop()
