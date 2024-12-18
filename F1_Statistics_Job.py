```python
import pyspark
from pyspark.sql import SparkSession
from pyspark.sql import functions as F

# Initialize Spark session for AWS Glue
spark = SparkSession.builder \
    .appName('Simplified_F1_Transformation') \
    .getOrCreate()

# Load the silver data from S3
silver_data = spark.read.parquet("s3://my-f1-data-bucket/silver_f1_data/")

simplified_data = silver_data.select(
    "stage_id",  
    "market_description",  # Using the column directly
    "name",  # Using the column directly
    "probability"  # Using the column directly
)

# Show the first few rows to verify
simplified_data.show(5)

# Save the simplified data to the gold layer
simplified_data.write.parquet("s3://my-f1-data-bucket/gold_f1_data/")
