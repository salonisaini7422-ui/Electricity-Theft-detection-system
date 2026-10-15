import sqlite3
import pandas as pd
from pathlib import Path

# Connect to the existing project database
DB_PATH = Path(__file__).with_name("electricity_data.db")

if not DB_PATH.exists():
    print("Database not found. Run the dashboard first.")
    raise SystemExit

with sqlite3.connect(DB_PATH) as conn:
    df = pd.read_sql_query(
        "SELECT * FROM readings",
        conn
    )

if df.empty:
    print("No readings found. Record readings in the dashboard first.")
else:
    print("\n===== ELECTRICITY THEFT DATA ANALYSIS =====")

    print("\nTotal readings:", len(df))

    print("\nStatus summary:")
    print(df["status"].value_counts())

    print("\nAverage supply power:")
    print(df["supply_power"].mean(), "W")

    print("\nAverage consumer power:")
    print(df["consumer_power"].mean(), "W")

    print("\nAverage power difference:")
    print(df["difference"].mean(), "W")

    print("\nRecent readings:")
    print(df.tail(10).to_string(index=False))

    # Save analysis data for documentation
    df.to_csv(
        Path(__file__).with_name("analysis_results.csv"),
        index=False
    )

    print("\nAnalysis exported to analysis_results.csv")