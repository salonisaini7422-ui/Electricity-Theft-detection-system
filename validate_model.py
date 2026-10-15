import sqlite3
import joblib
import pandas as pd
from pathlib import Path
from sklearn.metrics import accuracy_score, classification_report

BASE_DIR = Path(__file__).parent
DB_PATH = BASE_DIR / "electricity_data.db"
MODEL_PATH = BASE_DIR / "theft_model.pkl"

if not DB_PATH.exists() or not MODEL_PATH.exists():
    print("Database or trained model file is missing.")
    raise SystemExit

model = joblib.load(MODEL_PATH)

with sqlite3.connect(DB_PATH) as conn:
    df = pd.read_sql_query(
        "SELECT supply_power, consumer_power, difference, status "
        "FROM readings",
        conn
    )

if df.empty:
    print("No readings available for validation.")
    raise SystemExit

# Convert saved status into numeric labels
df["actual"] = df["status"].map({
    "Normal": 0,
    "Possible Theft": 1
})

df = df.dropna(subset=["actual"]).copy()

if df.empty or df["actual"].nunique() < 2:
    print("Record both Normal and Possible Theft readings first.")
    raise SystemExit

features = [
    "supply_power",
    "consumer_power",
    "difference"
]

df["prediction"] = model.predict(df[features])

print("\n===== MODEL VALIDATION =====")
print("Readings tested:", len(df))
print(
    "Agreement with saved status:",
    round(accuracy_score(df["actual"], df["prediction"]) * 100, 2),
    "%"
)

print("\nClassification Report:")
print(classification_report(
    df["actual"],
    df["prediction"],
    labels=[0, 1],
    target_names=["Normal", "Possible Theft"],
    zero_division=0
))

df.to_csv(
    BASE_DIR / "validation_results.csv",
    index=False
)

print("\nValidation results saved to validation_results.csv")