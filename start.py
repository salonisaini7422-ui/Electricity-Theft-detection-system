import time

print("Electricity Theft Detection System")
print("-" * 40)

# Set supply power and consumer readings
supply_power = 1000
consumers = {
    "Consumer 1": 400,
    "Consumer 2": 300,
    "Consumer 3": 300
}

while True:
    print("\nSupply Power:", supply_power, "W")

    total_consumer_power = 0

    for name, power in consumers.items():
        print(name + " Power:", power, "W")
        total_consumer_power += power

    power_difference = supply_power - total_consumer_power

    print("\nTotal Consumer Power:", total_consumer_power, "W")
    print("Power Difference:", power_difference, "W")

    if power_difference > 100:
        print("ALERT: Possible Electricity Theft!")
    else:
        print("STATUS: Normal")

    theft = input("\nSimulate theft? (yes/no/exit): ").lower()

    if theft == "yes":
        consumers["Consumer 3"] = 100
    elif theft == "no":
        consumers["Consumer 3"] = 300
    elif theft == "exit":
        print("System stopped.")
        break
    else:
        print("Invalid input. Enter yes, no, or exit.")

    time.sleep(1)