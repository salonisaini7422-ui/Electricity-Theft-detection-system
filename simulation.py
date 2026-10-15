import random
import time
from datetime import datetime
import database

# Initialize the database
database.init_db()

print("Electricity Theft Simulation Started")
print("Press Ctrl+C to stop.\n")

try:
    while True:
        # Simulated supply power
        supply_power = 1000

        # Simulated consumer readings
        consumers = {
            "Consumer 1": random.randint(280, 320),
            "Consumer 2": random.randint(280, 320),
            "Consumer 3": random.randint(280, 320)
        }

        # Occasionally simulate possible theft
        theft = random.random() < 0.3

        if theft:
            consumers["Consumer 3"] = random.randint(50, 150)

        consumer_power = sum(consumers.values())
        difference = supply_power - consumer_power

        status = (
            "Possible Theft"
            if difference > 100
            else "Normal"
        )

        current_time = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        # Save total and individual readings
        database.save_reading(
            current_time,
            supply_power,
            consumer_power,
            difference,
            status
        )

        database.save_consumer_readings(
            current_time,
            consumers,
            supply_power
        )

        print(
            f"{current_time} | "
            f"Supply: {supply_power} W | "
            f"Consumers: {consumer_power} W | "
            f"Difference: {difference} W | "
            f"Status: {status}"
        )

        time.sleep(5)

except KeyboardInterrupt:
    print("\nSimulation stopped.")