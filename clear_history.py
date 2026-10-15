import sqlite3
from pathlib import Path

db_path = Path(__file__).with_name("electricity_data.db")

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute("DELETE FROM readings")
cursor.execute("DELETE FROM consumer_readings")

conn.commit()
conn.close()

print("All old readings deleted successfully!")