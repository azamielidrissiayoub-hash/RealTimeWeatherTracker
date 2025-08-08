[README.md](https://github.com/user-attachments/files/21690082/README.md)
# 🌦️ Smart Weather Monitor

📊 **Real-Time Weather Monitoring System using Kafka, Spark, and Python**

---

## 📌 Description

This project collects real-time weather data from different Moroccan cities using a **Kafka producer**, processes it with **Spark Structured Streaming**, and provides:

- 🔁 Live temperature & humidity graphs (Matplotlib)
- 🔔 Alert system if temperature or humidity cross thresholds
- 💾 Storage of data in local CSVs (partitioned files)
- 📁 Organized folder structure with producers, consumers, and configs

---

## 🏗️ Architecture

```
┌──────────┐       ┌───────────────┐       ┌────────────────────┐
│ Producer │─────▶│ Kafka Broker   │─────▶│ Spark Consumer      │
└──────────┘       └───────────────┘       └────────────────────┘
                                                │
                                                ▼
                                       📈 Live Visualization
                                       💾 Save to CSV
                                       🔔 Alerts System
```

---

## 🗂️ Project Structure

```
Smart Weather Monitor/
├── config/              # Kafka config files
│   └── kafka_config.json
│
├── consumer/            # Spark Structured Streaming consumer
│   └── spark_stream_processor.py
│
├── producer/            # Weather producer (using OpenWeatherMap API or mock)
│   └── weather_producer.py
│
├── visualization/       # Real-time graph + alert system
│   └── alert_visualizer.py
│
├── data/                # Stored CSV outputs
│   └── weather/         # Auto-generated CSV files
│
├── requirements.txt     # Python dependencies
└── README.md            # 📄 You are here!
```

---

## ⚙️ Requirements

- Python 3.10+
- Kafka & ZooKeeper
- Spark (tested with PySpark 3.5.0)
- Matplotlib, Pandas
- `confluent_kafka` (Python client)

Install Python deps:

```bash
pip install -r requirements.txt
```

---

## 🚀 How to Run the Project

### 1. Start Kafka & Zookeeper (on Windows)

```bash
cd C:\kafka
.\bin\windows\zookeeper-server-start.bat .\config\zookeeper.properties
```

In new terminal:

```bash
cd C:\kafka
.\bin\windows\kafka-server-start.bat .\config\server.properties
```

### 2. Create Kafka topic (if not auto-created)

```bash
cd C:\kafka
.\bin\windows\kafka-topics.bat --create --topic weather --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1
```

---

### 3. Start the Kafka Producer

```bash
cd producer
python weather_producer.py
```

➡️ This sends weather data continuously to Kafka topic `weather`.

---

### 4. Start Spark Streaming Consumer

```bash
cd consumer
spark-submit spark_stream_processor.py
```

➡️ Spark listens to Kafka and stores data as CSV files inside `data/weather`.

---

### 5. Start Live Visualization with Alerts

```bash
cd visualization
python alert_visualizer.py
```

➡️ This will plot live temperature and humidity + show alerts like:

```
🔥 ALERT - Marrakesh temperature too high: 40.4°C
💧 ALERT - Marrakesh humidity too low: 17%
```

---

## 📈 Alert Thresholds

| Metric     | Threshold       |
|------------|-----------------|
| Temperature | ≥ 40°C (🔥)     |
| Humidity    | ≤ 20% (💧)       |

---

## 📁 Sample Output Files

Stored in: `data/weather/`

Each file: `part-xxxx.csv` with:

```csv
city,temperature,humidity,timestamp
Rabat,25.4,84.0,2025-08-08 18:30:12
```

---



---

## 👤 Author

Made with ❤️ by AYOUB AZAMI EL IDRISSI
