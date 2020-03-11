import logging
import json
from pyspark.sql import SparkSession
from pyspark.sql.types import *
import pyspark.sql.functions as psf


# TODO Create a schema for incoming resources
schema = StructType([
    StructField("crime_id", StringType(), True),
    StructField("original_crime_type_name", StringType(), True),
    StructField("report_date", StringType(), True),
    StructField("call_date", StringType(), True),
    StructField("offense_date", StringType(), True),
    StructField("call_time", StringType(), True),
    StructField("call_date_time", StringType(), True),
    StructField("disposition", StringType(), True),
    StructField("address", StringType(), True),
    StructField("city", StringType(), True),
    StructField("state", StringType(), True),
    StructField("agency_id", StringType(), True),
    StructField("address_type", StringType(), True),
    StructField("common_location", StringType(), True)
])

def run_spark_job(spark):

    # TODO Create Spark Configuration
    # Create Spark configurations with max offset of 200 per trigger
    # set up correct bootstrap server and port
    df = spark \
        .readStream \
        .format("kafka") \
        .option("subscribe", "com.deji.streams.crimes") \
        .option("startingOffsets", "earliest") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("maxRatePerPartition", 100) \
        .option("stopGracefullyOnShutdown", "true").load()
    # Show schema for the incoming resources for checks
    df.printSchema()

    # TODO extract the correct column from the kafka input resources
    # Take only value and convert it to String
    kafka_df = df.selectExpr("CAST(value AS STRING)")
    kafka_df.printSchema()
    service_table = kafka_df\
        .select(psf.from_json(psf.col('value'), schema).alias("DF"))\
        .select("DF.*")
    
    # TODO select original_crime_type_name and disposition
    distinct_table = service_table.select(['original_crime_type_name','disposition'])
    #service_table.select(['original_crime_type_name','disposition']).distinct()
    distinct_table.printSchema()

    # count the number of original crime type
    agg_df = distinct_table.dropna() \
        .select("original_crime_type_name") \
        .agg({"original_crime_type_name" : "count"}) \
        .orderBy("count(original_crime_type_name)", ascending=False)
    
    # TODO Q1. Submit a screen shot of a batch ingestion of the aggregation
    # TODO write output stream
    query = agg_df.writeStream.outputMode('complete').format('console').start()
            


    # TODO attach a ProgressReporter
    query.awaitTermination()

    # TODO get the right radio code json path
    radio_code_json_filepath = "./radio_code.json"
    radio_code_df = spark.read.json(radio_code_json_filepath)

    # clean up your data so that the column names match on radio_code_df and agg_df
    # we will want to join on the disposition code

    # TODO rename disposition_code column to disposition
    radio_code_df = radio_code_df.withColumnRenamed("disposition_code", "disposition").collect()

    # TODO join on disposition column
    join_query = agg_df.join(radio_code_df, radio_code_df.disposition == distinct_table.disposition)
    

    join_query.awaitTermination()

if __name__ == "__main__":
    logger = logging.getLogger(__name__)

    # TODO Create Spark in Standalone mode
    spark = SparkSession \
        .builder \
        .master("local[*]") \
        .config("spark.ui.port", "3000").config('spark.streaming.kafka.maxRatePerPartition', 300).config('spark.default.parallelism', 100).appName("KafkaSparkStructuredStreaming").getOrCreate()

    logger.info("Spark started")

    run_spark_job(spark)

    spark.stop()
