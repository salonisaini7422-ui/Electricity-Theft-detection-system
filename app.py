from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Dict

import database

# Create API application
app = FastAPI(
    title="Electricity Theft Detection API",
    description="Backend API for monitoring electricity usage",
    version="1.0.0"
)

# Initialize existing database
database.init_db()


# Request format for incoming readings
class ReadingInput(BaseModel):
    supply_power: float = Field(gt=0)
    consumers: Dict[str, float]


# Home endpoint
@app.get("/")
def home():
    return {
        "message": "Electricity Theft Detection API is running",
        "docs": "/docs"
    }


# Health check
@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "database": "initialized"
    }


# Receive and save a new reading
@app.post("/readings")
def create_reading(data: ReadingInput):

    if not data.consumers:
        raise HTTPException(
            status_code=400,
            detail="At least one consumer is required"
        )

    if any(power < 0 for power in data.consumers.values()):
        raise HTTPException(
            status_code=400,
            detail="Consumer power cannot be negative"
        )

    consumer_power = sum(data.consumers.values())
    difference = data.supply_power - consumer_power

    status = (
        "Possible Theft"
        if difference > 100
        else "Normal"
    )

    current_time = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    # Save total reading
    database.save_reading(
        current_time,
        data.supply_power,
        consumer_power,
        difference,
        status
    )

    # Save individual consumer readings
    database.save_consumer_readings(
        current_time,
        data.consumers,
        data.supply_power
    )

    return {
        "message": "Reading saved successfully",
        "time": current_time,
        "supply_power": data.supply_power,
        "consumer_power": consumer_power,
        "power_difference": difference,
        "status": status,
        "consumers": data.consumers
    }


# Get all saved total readings
@app.get("/readings")
def get_all_readings():
    return database.get_readings()


# Get individual consumer history
@app.get("/consumers")
def get_all_consumers():
    return database.get_consumer_readings()


# Get possible theft alerts
@app.get("/alerts")
def get_alerts():
    readings = database.get_readings()

    alerts = [
        reading for reading in readings
        if reading["Status"] == "Possible Theft"
    ]

    return {
        "total_alerts": len(alerts),
        "alerts": alerts
    }