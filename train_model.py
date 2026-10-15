import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib

# Sample training data for demonstration
data = {
    "supply_power": [
        1000, 1000, 1000, 1000, 1000,
        1000, 1000, 1000, 1000, 1000,
        1000, 1000, 1000, 1000, 1000,
        1000, 1000, 1000, 1000, 1000
    ],
    "consumer_power": [
        950, 920, 970, 940, 960,
        700, 650, 720, 680, 750,
        930, 910, 980, 950, 920,
        600, 700, 650, 750, 680
    ],
    "difference": [
        50, 80, 30, 60, 40,
        300, 350, 280, 320, 250,
        70, 90, 20, 50, 80,
        400, 300, 350, 250, 320
    ],
    "theft": [
        0, 0, 0, 0, 0,
        1, 1, 1, 1, 1,
        0, 0, 0, 0, 0,
        1, 1, 1, 1, 1
    ]
}

df = pd.DataFrame(data)

# Features and target
X = df[["supply_power", "consumer_power", "difference"]]
y = df["theft"]

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.25,
    random_state=42,
    stratify=y
)

# Train the model
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)
model.fit(X_train, y_train)

# Evaluate the model
predictions = model.predict(X_test)
print("Model training completed!")
print("Accuracy:", accuracy_score(y_test, predictions))
print("\nClassification Report:")
print(classification_report(y_test, predictions, zero_division=0))

# Save the trained model
joblib.dump(model, "theft_model.pkl")
print("\nModel saved as theft_model.pkl")