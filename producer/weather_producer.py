from confluent_kafka import Producer
import requests
import json
import time
from datetime import datetime

API_KEY = "bd5e378503939ddaee************"
TOPIC = "weather_data"
BROKER = "localhost:9092"
CITIES_FILE = "../config/cities.txt"

producer = Producer({'bootstrap.servers': BROKER})

def delivery_report(err, msg):
    if err is not None:
        print(f"❌ Delivery failed: {err}")
    else:
        print(f"✅ Sent to {msg.topic()} [{msg.partition()}]")

with open(CITIES_FILE, "r") as file:
    cities = [line.strip() for line in file.readlines() if line.strip()]

while True:
    for city in cities:
        try:
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
            response = requests.get(url)
            data = response.json()

            print(f"📦 Response for {city}:\n", data)  # ⬅️ أضف هذا


            weather_info = {
                "city": city.title(),
                "temperature": data["main"]["temp"],
                "humidity": data["main"]["humidity"],
                "timestamp": datetime.utcnow().isoformat()
            }

            producer.produce(
                TOPIC,
                key=city,
                value=json.dumps(weather_info),
                callback=delivery_report
            )
            producer.poll(1)
        except Exception as e:
            print(f"⛔ Error fetching weather for {city}: {e}")

    time.sleep(10)
