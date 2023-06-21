from pyspark.sql import SparkSession
import os

# Get the current working directory
current_dir = os.getcwd()

# Path to the JAR file in the project's lib directory
jdbc_driver_path = f"{current_dir}/lib/postgresql-42.6.0.jar"

# Create SparkSession
spark = SparkSession.builder \
    .appName("llava-api-etl") \
    .config("spark.driver.extraClassPath", jdbc_driver_path) \
    .config("spark.executor.extraClassPath", jdbc_driver_path) \
    .getOrCreate()
