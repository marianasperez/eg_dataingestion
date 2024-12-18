**Code Explanation**:
   ```python
   import pyspark
   from pyspark.sql import SparkSession
   from pyspark.sql.functions import explode, col

   # Initialize Spark session
   spark = SparkSession.builder.appName('F1DataTransformation').getOrCreate()

   # Load the raw data from the S3 location (Raw layer)
   raw_data = spark.read.json("s3://my-f1-data-bucket/")

   # Simplified data transformation:
   cleaned_data = raw_data.select(
       col("stage.id").alias("stage_id"),  # Renaming to avoid ambiguity
       col("stage.description").alias("stage_description"),  # Renaming to avoid ambiguity
       explode("probabilities.markets").alias("market")  # Exploding the markets array
   ).select(
       "stage_id",  # Stage ID
       "stage_description",  # Stage Description
       col("market.description").alias("market_description"),  # Renaming to avoid ambiguity
       explode("market.outcomes").alias("outcome")  # Exploding outcomes
   ).select(
       "stage_id", 
       "stage_description", 
       "market_description", 
       "outcome.id",  # Outcome ID
       "outcome.name",  # Outcome Name
       "outcome.probability"  # Outcome Probability
   )

   # Write the cleaned data to Parquet format to S3 (Silver Layer)
   cleaned_data.write.parquet("s3://my-f1-data-bucket/silver_f1_data/")
