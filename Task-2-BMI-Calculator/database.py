import sqlite3

# Connect to database
connection = sqlite3.connect("bmi.db")

# Create cursor
cursor = connection.cursor()

# Create table
cursor.execute("""
CREATE TABLE IF NOT EXISTS bmi_records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    weight REAL,
    height REAL,
    bmi REAL,
    category TEXT
)
""")

# Save changes
connection.commit()

# Close database
connection.close()