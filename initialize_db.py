import sqlite3

# Path to the database
db_path = 'database.db'

# Connect to the database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Drop existing tables if they exist
cursor.execute("DROP TABLE IF EXISTS students;")

# Create new tables with additional fields
create_students_table = '''
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    code_rim TEXT NOT NULL,
    gender TEXT NOT NULL,
    date_of_register TEXT NOT NULL,
    classroom TEXT NOT NULL,
    price REAL NOT NULL,
    number_of_agent INTEGER NOT NULL
);
'''

# Execute the query to create the table
cursor.execute(create_students_table)

# Commit the changes and close the connection
conn.commit()
conn.close()

print("Database updated successfully.")
