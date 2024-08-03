import sqlite3

# Path to the database
db_path = 'database.db'

# Connect to the database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Drop existing tables if they exist
cursor.execute("DROP TABLE IF EXISTS students;")
cursor.execute("DROP TABLE IF EXISTS classrooms;")

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

create_classrooms_table = '''
CREATE TABLE IF NOT EXISTS classrooms (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    level TEXT NOT NULL,
    type TEXT NOT NULL,
    subjects TEXT
);
'''

# Execute the queries to create the tables
cursor.execute(create_students_table)
cursor.execute(create_classrooms_table)

# Commit the changes and close the connection
conn.commit()
conn.close()

print("Database updated successfully.")
