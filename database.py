import sqlite3
from pathlib import Path

# Database file will be created in this project folder
DB_PATH = Path(__file__).with_name("electricity_data.db")


def init_db():
    """Create all required database tables."""
    with sqlite3.connect(DB_PATH) as conn:

        # Table for total readings
        conn.execute("""
            CREATE TABLE IF NOT EXISTS readings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                time TEXT NOT NULL,
                supply_power REAL NOT NULL,
                consumer_power REAL NOT NULL,
                difference REAL NOT NULL,
                status TEXT NOT NULL
            )
        """)

        # Table for individual consumer readings
        conn.execute("""
            CREATE TABLE IF NOT EXISTS consumer_readings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                time TEXT NOT NULL,
                consumer_name TEXT NOT NULL,
                power REAL NOT NULL,
                status TEXT NOT NULL
            )
        """)
def save_consumer_readings(time, consumers, supply_power):
    """Save each consumer's reading separately."""
    total_power = sum(consumers.values())
    difference = supply_power - total_power

    # Decide status based on the power difference
    if difference > 300:
        status = "Possible Theft"
    elif difference > 100:
        status = "Review Required"
    else:
        status = "Normal"

    with sqlite3.connect(DB_PATH) as conn:
        for name, power in consumers.items():
            conn.execute("""
                INSERT INTO consumer_readings (
                    time, consumer_name, power, status
                )
                VALUES (?, ?, ?, ?)
            """, (time, name, power, status))


def get_consumer_readings():
    """Retrieve saved individual consumer readings."""
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row

        rows = conn.execute("""
            SELECT
                time AS 'Time',
                consumer_name AS 'Consumer',
                power AS 'Power (W)',
                status AS 'Status'
            FROM consumer_readings
            ORDER BY id DESC
        """).fetchall()

        return [dict(row) for row in rows]
    
def save_reading(time, supply_power, consumer_power,
                 difference, status):
    """Save one reading permanently."""
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            INSERT INTO readings (
                time, supply_power, consumer_power,
                difference, status
            )
            VALUES (?, ?, ?, ?, ?)
        """, (
            time, supply_power, consumer_power,
            difference, status
        ))


def get_readings():
    """Retrieve all saved readings."""
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row

        rows = conn.execute("""
            SELECT
                time AS 'Time',
                supply_power AS 'Supply (W)',
                consumer_power AS 'Consumer (W)',
                difference AS 'Difference (W)',
                status AS 'Status'
            FROM readings
            ORDER BY id DESC
        """).fetchall()

        return [dict(row) for row in rows]


# Initialize the database and table
if __name__ == "__main__":
    init_db()
    print("Database initialized successfully!")
    print("Database location:", DB_PATH)
    