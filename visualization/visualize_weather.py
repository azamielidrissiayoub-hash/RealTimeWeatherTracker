import pandas as pd
import matplotlib.pyplot as plt
import os
import time

# 📁 Absolute or relative path to weather CSV files
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # this file's dir
DATA_DIR = os.path.join(BASE_DIR, "..", "data", "weather")

# 🚨 Alert Thresholds
TEMP_ALERT_THRESHOLD = 40      # °C
HUMIDITY_ALERT_THRESHOLD = 20  # %

# 📈 Live plot mode
plt.ion()
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))

while True:
    try:
        # 📥 Load all CSV files in the folder
        all_files = [
            os.path.join(DATA_DIR, f)
            for f in os.listdir(DATA_DIR)
            if f.endswith(".csv")
        ]

        if not all_files:
            print("📂 No CSV files found.")
            time.sleep(2)
            continue

        # 📊 Combine all CSVs into one DataFrame
        df = pd.concat(
            (pd.read_csv(f, header=None, names=["city", "temperature", "humidity", "timestamp"]) for f in all_files),
            ignore_index=True
        )

        # 🕒 Clean timestamps
        df["timestamp"] = pd.to_datetime(df["timestamp"], errors='coerce')
        df = df.dropna(subset=["timestamp"])  # drop invalid timestamps
        df = df.sort_values("timestamp")

        # 🔁 Clear previous plots
        ax1.clear()
        ax2.clear()

        for city in df["city"].unique():
            city_df = df[df["city"] == city]

            # 📈 Plot temperature and humidity
            ax1.plot(city_df["timestamp"], city_df["temperature"], label=city)
            ax2.plot(city_df["timestamp"], city_df["humidity"], label=city)

            # 🚨 Alert system on latest values
            latest = city_df.iloc[-1]

            temp = latest["temperature"]
            hum = latest["humidity"]
            city_name = latest["city"]
            ts = latest["timestamp"]

            if temp >= TEMP_ALERT_THRESHOLD:
                print(f"🔥 ALERT [{ts}] - {city_name}: High temperature ({temp}°C)")

            if hum <= HUMIDITY_ALERT_THRESHOLD:
                print(f"💧 ALERT [{ts}] - {city_name}: Low humidity ({hum}%)")

        # 🖼️ Customize plot
        ax1.set_title("🌡️ Temperature Over Time")
        ax1.set_ylabel("Temperature (°C)")
        ax1.legend()
        ax1.grid(True)

        ax2.set_title("💧 Humidity Over Time")
        ax2.set_ylabel("Humidity (%)")
        ax2.legend()
        ax2.grid(True)

        plt.tight_layout()
        plt.pause(2)  # wait 2s before refreshing

    except Exception as e:
        print("⛔ Error:", e)
        time.sleep(2)
