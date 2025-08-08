from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StringType, DoubleType

spark = SparkSession.builder \
    .appName("WeatherStreamProcessor") \
    .master("local[*]") \
    .getOrCreate()

KAFKA_BOOTSTRAP = "localhost:9092"
KAFKA_TOPIC = "weather_data"

schema = StructType() \
    .add("city", StringType()) \
    .add("temperature", DoubleType()) \
    .add("humidity", DoubleType()) \
    .add("timestamp", StringType())

df_kafka_raw = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", KAFKA_BOOTSTRAP) \
    .option("subscribe", KAFKA_TOPIC) \
    .option("startingOffsets", "latest") \
    .load()

df_kafka_str = df_kafka_raw.selectExpr("CAST(value AS STRING)")

df_weather = df_kafka_str.select(
    from_json(col("value"), schema).alias("data")
).select("data.*")

query = df_weather.writeStream \
    .outputMode("append") \
    .format("csv") \
    .option("path", "../data/weather") \
    .option("checkpointLocation", "../data/weather_checkpoint") \
    .start()

query.awaitTermination()
