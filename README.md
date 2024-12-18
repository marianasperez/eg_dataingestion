# eg_dataingestion
# F1 Data Ingestion and Transformation

## 1. Overview

This project uses the **F1 API** from **SportsRadar** to retrieve F1 race data and processes it through an ETL pipeline using **AWS Lambda**, **AWS Glue**, and **AWS S3**. The data is processed using the **medallion architecture** (raw, silver, and gold layers), with the goal of transforming and simplifying the F1 data for analysis and reporting.

The data is automatically ingested from the API daily using **EventBridge**, and the cleaned and transformed data is stored in **Parquet format** in an S3 bucket. 

## 2. API and Data Retrieval

- **API Chosen**: F1 data from **SportsRadar** API.
- **API Endpoint**: `Stage Probabilities`.
- **API Key**: Created an account with SportsRadar to obtain the API key.
  
A function called **F1DataIngestion** was created in **AWS Lambda**. The function purpuse is retrieves data from the API and saves it to **AWS S3** in a JSON file. 

## 3. Lambda Function and Permissions

- **Function**: `F1DataIngestion`
- **Code**: The Python code for the Lambda function can be found in **`eg_dataingestion/lambda_function.py`** under the GitHub repository.
- **Permissions**: The required permissions were set for Lambda to allow **EventBridge** to invoke it using the **allow-eventbridge-to-invoke-lambda** policy.

Before deploying the Lambda function, an **S3 bucket** called **`my-f1-data-bucket`** was created to store the raw data. Once deployed, the function created a **JSON file** (`f1_data_2024-12-18.json`) under the S3 bucket.

## 4. ETL Process with AWS Glue

The ETL process was implemented using **AWS Glue** with the **medallion architecture**, which includes the following layers:

1. **Raw Layer**: The raw data is imported directly from the API and saved as JSON.
2. **Silver Layer**: The raw data is transformed, cleaned, and written to Parquet format.
3. **Gold Layer**: The silver data is simplified further and saved in the gold layer for final reporting.

### 4.1 Crawler Setup

- **Crawler**: **`F1DataCrawler`** was created in AWS Glue to crawl the S3 bucket (`s3://my-f1-data-bucket`) for raw data.
- **Target Database**: **`f1_raw_data_db`** was created to store the raw data.

### 4.2 Jobs Setup

Two AWS Glue jobs were created to process the data:

1. **F1DataTransformation**: 
   - **Code**: The Python code for this job is stored in the GitHub repository under **`F1DataTransformation.py`**.
   - The **F1DataTransformation** job is responsible for transforming the raw data retrieved from the F1 API. This transformation includes renaming columns, exploding arrays, and cleaning the data. One key part of this transformation is converting the data from its original **JSON** format to **Parquet** format. The cleaned data is then written to the **Silver layer** in Parquet format under the S3 bucket.

2. **F1_Statistics_Job**

 - **Code**: The Python code for this job is stored in the GitHub repository under **`F1_Statistics_Job.py`**.
 - The **F1_Statistics_Job** simplifies the data further by selecting only the relevant columns and writing the final dataset to the **Gold layer** in **Parquet** format. The job uses **AWS Glue** to read the silver data, process it, and store the simplified data for downstream analysis.

## 5. EventBridge & Schedule for Automation

To automate the daily ingestion of F1 data, an **EventBridge** rule called **`F1InvokeDaily`** was created. This rule invokes the **F1DataIngestion** Lambda function every day at **midnight**, ensuring that the latest F1 data is ingested and processed without manual intervention.

Additionally, schedules were added under **AWS Glue Jobs** for updates at **1 AM**, following the completion of the raw data ingestion process. This ensures that the data transformation and cleaning steps in the **Silver** and **Gold** layers are performed promptly after the raw data is ingested.

By using **EventBridge**, the entire process of retrieving data from the API, transforming it, and storing it in the S3 bucket is automated, enabling real-time data updates for further analysis.

## 6. Results under S3

After the data has been processed by the **F1DataTransformation** and **F1_Statistics_Job** jobs, the final output is stored in **Parquet format** in the following locations within the S3 bucket:

- **Raw Data**: `s3://my-f1-data-bucket/`
- **Silver Data**: `s3://my-f1-data-bucket/silver_f1_data/`
- **Gold Data**: `s3://my-f1-data-bucket/gold_f1_data/`

This structured data is now available for further analysis, reporting, or future enhancements, such as integration with query tools or visualization platforms.
- You can see the results under `S3 Bucket & Objects Results.png `

## 7. Assumptions

The transformation process from **JSON** to **Parquet**:

1. **Improved Performance**:
   - **Parquet** is a columnar storage format, meaning it stores data by columns instead of rows. This allows for more efficient queries, especially when only specific columns are needed. In contrast, **JSON** stores data in a row-based format, which can be slower for large datasets when only a subset of columns is required.

2. **Better Compression**:
   - **Parquet** is more efficient at compressing data compared to **JSON**, which results in reduced storage costs. This is especially beneficial when dealing with large datasets like F1 race data, as Parquet helps reduce the amount of disk space needed.

3. **Schema Support**:
   - **Parquet** files are schema-aware, ensuring the structure of the data is preserved. This makes the data easier to manage, maintain, and analyze. **JSON**, on the other hand, is a flexible format and lacks this level of schema enforcement, which can make it harder to ensure consistent data structure over time.

4. **Optimized for Big Data Processing**:
   - **Parquet** is designed to work efficiently in distributed data processing systems like **Apache Spark** and **AWS Glue**. These tools can process **Parquet** files in parallel, significantly improving the speed and efficiency of the ETL process, especially when handling large amounts of data.

5. **Compatibility with Analytics Tools**:
   - **Parquet** is natively supported by many analytics tools, including **AWS Athena**, **Presto**, **Apache Hive**, and **Tableau**. Storing data in Parquet format ensures compatibility with these tools, making it easier to query and analyze the data for further reporting and visualization.

By converting the raw data into **Parquet**, the transformation process improves performance, reduces storage costs, and ensures the data is in a format optimized for future analysis and querying.


## 8. Future Improvements

- **Athena Integration**: In the future, use **AWS Athena** to query the Gold layer data directly from S3 for further analysis and reporting.
- **Tableau Integration**: The processed F1 data can be integrated with **Tableau** for visualizations and dashboards to provide interactive insights into the F1 race data.
- **Data Integrity**: Future improvements will include adding data validation to ensure the quality of the data.
