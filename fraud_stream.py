
# fraud_stream.py -- PySpark Structured Streaming skeleton (rule-based)
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, when, unix_timestamp, lag
from pyspark.sql.types import StructType, StringType, DoubleType
from pyspark.sql.window import Window

schema = StructType()     .add("txn_id", StringType())     .add("user_id", StringType())     .add("amount", DoubleType())     .add("merchant", StringType())     .add("location", StringType())     .add("timestamp", StringType())

spark = SparkSession.builder.appName("CreditCardFraudDetectionRuleBased").getOrCreate()

raw = spark.readStream.format("kafka")     .option("kafka.bootstrap.servers", "localhost:9092")     .option("subscribe", "credit_txn_stream")     .load()

txns = raw.select(from_json(col("value").cast("string"), schema).alias("data")).select("data.*")

# Rule 1: amount > 15000
txns = txns.withColumn("flag_amount", col("amount") > 15000)

# For rapid transactions rule, use stateful processing or windowed aggregates in production.

txns_with_flag = txns.withColumn("fraud_flag", when(col("flag_amount"), "POTENTIAL_FRAUD").otherwise("LEGIT"))

query = txns_with_flag.writeStream.format("console").outputMode("append").start()
query.awaitTermination()
