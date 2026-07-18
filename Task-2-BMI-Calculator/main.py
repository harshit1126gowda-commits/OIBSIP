import tkinter as tk
from tkinter import messagebox
import sqlite3
from tkinter.font import names
import matplotlib.pyplot as plt

# Function to view BMI history
def view_history():
    connection = sqlite3.connect("bmi.db")
    cursor = connection.cursor()

    cursor.execute("SELECT name, weight, height, bmi, category FROM bmi_records")
    records = cursor.fetchall()

    history_window = tk.Toplevel(root)
    history_window.title("BMI History")
    history_window.geometry("500x400")

    heading = tk.Label(history_window, text="BMI History", font=("Arial", 16, "bold"))
    heading.pack(pady=10)

    text = tk.Text(history_window, width=60, height=20)
    text.pack()

    for record in records:
        text.insert(
            tk.END,
            f"Name: {record[0]}\n"
            f"Weight: {record[1]} kg\n"
            f"Height: {record[2]} m\n"
            f"BMI: {record[3]:.2f}\n"
            f"Category: {record[4]}\n"
            "-----------------------------\n"
        )

    connection.close()
    def show_bmi_graph():
        import sqlite3
        conn = sqlite3.connect("bmi.db")
        cursor = conn.cursor()
        cursor.execute("SELECT name, bmi FROM bmi_records")
        records = cursor.fetchall()
        conn.close()
        if len(records) == 0:
            messagebox.showinfo("No Data", "No BMI records available")
            return
        names = []
        bmi_values = []
        for record in records:
            names.append(record[0])
            bmi_values.append(record[1])
            plt.figure(figsize=(8,5))
            plt.plot(names, bmi_values, marker="o")
            plt.xlabel("Names")
        plt.ylabel("BMI Values")
        plt.title("BMI History Graph")
        plt.xticks(rotation=45)
    plt.grid(True)
    plt.show()
# Function to calculate BMI
def calculate_bmi():
    try:
        name = name_entry.get()

        weight = float(weight_entry.get())
        height = float(height_entry.get())

        if weight <= 0 or height <= 0:
            messagebox.showerror("Error", "Weight and Height must be greater than zero!")
            return

        bmi = weight / (height * height)

        if bmi < 18.5:
            category = "Underweight"
        elif bmi < 25:
            category = "Normal Weight"
        elif bmi < 30:
            category = "Overweight"
        else:
            category = "Obese"

        result_label.config(
            text=f"Hello {name}\n\nBMI : {bmi:.2f}\nCategory : {category}",
            fg="blue"
        )
        # Save data into database
        connection = sqlite3.connect("bmi.db")
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO bmi_records(name, weight, height, bmi, category) VALUES (?, ?, ?, ?, ?)",
            (name, weight, height, bmi, category)
        )
        connection.commit()
        connection.close()
    except ValueError:
        messagebox.showerror("Error", "Please enter valid values!")

# Function to reset fields
def reset():
    name_entry.delete(0, tk.END)
    weight_entry.delete(0, tk.END)
    height_entry.delete(0, tk.END)
    result_label.config(text="")
def show_bmi_graph():
    conn = sqlite3.connect("bmi.db")
    cursor = conn.cursor()

    cursor.execute("SELECT name, bmi FROM bmi_records")
    records = cursor.fetchall()

    conn.close()

    if len(records) == 0:
        messagebox.showinfo("No Data", "No BMI records available")
        return

    names = []
    bmi_values = []

    for record in records:
        names.append(record[0])
        bmi_values.append(record[1])

    plt.figure(figsize=(8,5))
    plt.plot(names, bmi_values, marker="o")

    plt.xlabel("Names")
    plt.ylabel("BMI Values")
    plt.title("BMI History Graph")

    plt.xticks(rotation=45)
    plt.grid(True)

    plt.show()

def delete_history():
    conn = sqlite3.connect("bmi.db")
    cursor = conn.cursor()

    cursor.execute("DELETE FROM bmi_records")

    conn.commit()
    conn.close()

    messagebox.showinfo("Deleted", "All BMI history deleted successfully")
def search_bmi():
    search_name = name_entry.get().strip()

    conn = sqlite3.connect("bmi.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM bmi_records WHERE LOWER(name)=LOWER(?)",
        (search_name,)
    )

    records = cursor.fetchall()
    conn.close()

    if records:
        result = ""
        for row in records:
            result += f"Name: {row[1]}, Weight: {row[2]} kg, Height: {row[3]} m, BMI: {row[4]}\n"
            messagebox.showinfo("Search Result", result)
        else:
            messagebox.showinfo("No Result", "No record found")

# Main Window
root = tk.Tk()
root.title("BMI Calculator-Health Tracker")
root.geometry("400x600")
root.resizable(False, False)
root.configure(bg="#E8F6F3")

# Heading
title = tk.Label(
    root,
    text="BMI Calculator",
    font=("Arial", 20, "bold"),
   
)
title.pack(pady=20)
name_label = tk.Label(
    root,
    text="Name",
    font=("Arial", 12)
)
name_label.pack()

name_entry = tk.Entry(root, width=30)
name_entry.pack(pady=5)


weight_label = tk.Label(
    root,
    text="Weight (kg)",
    font=("Arial", 12)
)
weight_label.pack()

weight_entry = tk.Entry(root, width=30)
weight_entry.pack(pady=5)


height_label = tk.Label(
    root,
    text="Height (m)",
    font=("Arial", 12)
)
height_label.pack()

height_entry = tk.Entry(root, width=30)
height_entry.pack(pady=5)


# Calculate Button
calculate_button = tk.Button(
    root,
    text="Calculate BMI",
    command=calculate_bmi,
    bg="blue",
    fg="white",
    width=20,
    font=("Arial", 11, "bold")
)

calculate_button.pack(pady=8)


# Reset Button
reset_button = tk.Button(
    root,
    text="Reset",
    command=reset,
    bg="gray",
    fg="white",
    width=20,
    font=("Arial", 11, "bold")
)

reset_button.pack(pady=8)

history_button = tk.Button(
    root,
    text="View History",
    command=view_history,
    bg="purple",
    fg="white",
    width=20,
    font=("Arial", 11, "bold")
)

history_button.pack(pady=8)

graph_button = tk.Button(
    root,
    text="Show BMI Graph",
    command=show_bmi_graph,
    bg="green",
    fg="white",
    width=20,
    font=("Arial", 11, "bold")
)

graph_button.pack(pady=8)

# Result
result_label = tk.Label(
    root,
    text="",
    font=("Arial", 13, "bold"),
    bg="#E8F6F3"
)
result_label.pack(pady=20)
delete_button = tk.Button(
    root,
    text="Delete History",
    command=delete_history,
    bg="red",
    fg="white",
    width=20,
    font=("Arial", 11, "bold")
)

delete_button.pack(pady=8)

search_button = tk.Button(
    root,
    text="Search by Name",
    command=search_bmi,
    bg="orange",
    fg="black",
    width=20,
    font=("Arial", 11, "bold")
)

search_button.pack(pady=8)
# Run Application
root.mainloop()