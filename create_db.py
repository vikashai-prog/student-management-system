import sqlite3

conn = sqlite3.connect("database.db")

conn.execute("CREATE TABLE IF NOT EXISTS students (roll TEXT, name TEXT, age TEXT)")

conn.close()

print("Database ready ✅")