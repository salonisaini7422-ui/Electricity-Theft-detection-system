import streamlit as st
import pandas as pd
from datetime import datetime
import database
from streamlit_autorefresh import st_autorefresh
import joblib
from pathlib import Path
# Page configuration
st.set_page_config(
    page_title="Electricity Theft Detection System",
    page_icon="⚡",
    layout="wide"
)
st_autorefresh(
    interval=5000,
    key="dashboard_refresh"
)
# Load trained Machine Learning model

MODEL_PATH = Path(__file__).with_name("theft_model.pkl")

if MODEL_PATH.exists():
    model = joblib.load(MODEL_PATH)
else:
    model = None
    st.warning("ML model file not found. Please train the model first.")
# Initialize database
database.init_db()

# Dashboard heading
st.title("⚡ Electricity Theft Detection System")
st.caption("Smart Energy Monitoring and Theft Alert Dashboard")
st.divider()

# -------------------------------
# 1. CONTROL PANEL
# -------------------------------
st.subheader("Control Panel")

theft_mode = st.toggle(
    "Simulate Electricity Theft",
    value=False
)

# Supply power
supply_power = 1000

# Distributive consumer data (Watts)
consumers = {
    "Consumer 1": 300,
    "Consumer 2": 300,
    "Consumer 3": 400
}

# Simulate theft in Consumer 3
if theft_mode:
    consumers["Consumer 3"] = 100

# Calculate total consumer power
consumer_power = sum(consumers.values())

# Calculate power difference
power_difference = supply_power - consumer_power
# -------------------------------
# MACHINE LEARNING PREDICTION
# -------------------------------
ml_prediction = None
ml_confidence = None

if model is not None:
    input_data = pd.DataFrame(
        [[supply_power, consumer_power, power_difference]],
        columns=[
            "supply_power",
            "consumer_power",
            "difference"
        ]
    )

    ml_prediction = int(model.predict(input_data)[0])

    if hasattr(model, "predict_proba"):
        probabilities = model.predict_proba(input_data)[0]
        ml_confidence = float(max(probabilities)) * 100
# -------------------------------
# 2. TOTAL POWER READINGS
# -------------------------------
st.subheader("Total Power Readings")

col1, col2, col3 = st.columns(3)

col1.metric(
    "Supply Power",
    f"{supply_power} W"
)

col2.metric(
    "Total Consumer Power",
    f"{consumer_power} W"
)

col3.metric(
    "Power Difference",
    f"{power_difference} W"
)

st.divider()

# -------------------------------
# 3. INDIVIDUAL CONSUMER READINGS
# -------------------------------
st.subheader("Individual Consumer Readings")

c1, c2, c3 = st.columns(3)

c1.metric(
    "Consumer 1",
    f"{consumers['Consumer 1']} W"
)

c2.metric(
    "Consumer 2",
    f"{consumers['Consumer 2']} W"
)

c3.metric(
    "Consumer 3",
    f"{consumers['Consumer 3']} W"
)

# Display consumer distribution
st.subheader("Consumer Power Distribution")

consumer_df = pd.DataFrame({
    "Consumer": list(consumers.keys()),
    "Power (W)": list(consumers.values())
})

st.dataframe(
    consumer_df,
    use_container_width=True,
    hide_index=True
)

st.divider()

# -------------------------------
# 4. THEFT DETECTION ALERT
# Display alert according to power difference
if power_difference > 300:
    st.error("🚨 HIGH ALERT: Possible Electricity Theft Detected!")
elif power_difference > 100:
    st.warning("⚠️ WARNING: Suspicious Power Difference Detected!")
else:
    st.success("✅ Normal: No Suspicious Power Difference Detected.")

# -------------------------------
# MACHINE LEARNING RESULT
# -------------------------------
st.subheader("🤖 Machine Learning Prediction")

if ml_prediction is not None:
    if ml_prediction == 1:
        st.error("ML Prediction: Possible Theft")
    else:
        st.success("ML Prediction: Normal")

    if ml_confidence is not None:
        st.metric(
            "Model Confidence",
            f"{ml_confidence:.1f}%"
        )
else:
    st.warning("Machine Learning model is not loaded.")
st.info("Total and individual consumer readings saved successfully!")
# -------------------------------
# 5. SAVE READINGS TO DATABASE
# -------------------------------
if st.button("Record Current Reading"):

    status = (
        "Possible Theft"
        if power_difference > 100
        else "Normal"
    )

    current_time = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    # Save total power reading
    database.save_reading(
        current_time,
        supply_power,
        consumer_power,
        power_difference,
        status
    )

    # Save individual consumer readings
    database.save_consumer_readings(
        current_time,
        consumers,
        supply_power
    )

    st.success(
        "Total and individual consumer readings saved successfully!"
    )

# -------------------------------
# 6. POWER MONITORING GRAPH
# -------------------------------
st.divider()
st.subheader("📊 Power Monitoring Graph")

graph_data = pd.DataFrame({
    "Power Type": [
        "Supply",
        "Consumer 1",
        "Consumer 2",
        "Consumer 3"
    ],
    "Power (W)": [
        supply_power,
        consumers["Consumer 1"],
        consumers["Consumer 2"],
        consumers["Consumer 3"]
    ]
})

st.bar_chart(
    graph_data,
    x="Power Type",
    y="Power (W)"
)

# -------------------------------
# 7. TOTAL READING HISTORY
# -------------------------------
st.divider()
st.subheader("📋 Total Reading History")

history = database.get_readings()

if history:
    history_df = pd.DataFrame(history)

    st.dataframe(
        history_df,
        use_container_width=True
    )

    csv_data = history_df.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        label="Download Total History (CSV)",
        data=csv_data,
        file_name="electricity_reading_history.csv",
        mime="text/csv"
    )
else:
    st.info(
        "No readings recorded yet. Click 'Record Current Reading'."
    )

# -------------------------------
# 8. INDIVIDUAL CONSUMER HISTORY
# -------------------------------
st.divider()
st.subheader("👥 Individual Consumer History")

consumer_history = database.get_consumer_readings()

if consumer_history:
    consumer_history_df = pd.DataFrame(
        consumer_history
    )

    st.dataframe(
        consumer_history_df,
        use_container_width=True
    )

    consumer_csv = consumer_history_df.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        label="Download Consumer History (CSV)",
        data=consumer_csv,
        file_name="individual_consumer_history.csv",
        mime="text/csv"
    )
else:
    st.info(
        "No individual consumer readings saved yet."
    )

# Footer
st.divider()
st.caption(
    "Demo simulation only. No real sensors are connected."
)