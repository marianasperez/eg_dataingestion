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

## 7. Role and Policy Management
To ensure proper access between the various AWS services (such as Lambda, Glue, and S3), I created specific IAM roles with the necessary permissions. 
These roles were designed to enable secure interactions between the services while maintaining the principle of least privilege. 
For example, the Lambda function required permission to read from the API, write to S3, and trigger the Glue jobs. I configured a custom IAM policy called allow-eventbridge-to-invoke-lambda to allow EventBridge to trigger the Lambda function daily.
Similarly, the AWS Glue jobs were granted access to read from the raw data in S3, process the data, and write the transformed data back to S3. These roles and policies were configured to ensure that only the necessary services could access specific resources, providing secure and controlled access between the applications.

- See `Policy_example` & `IAM Roles.png`
  
## 8. Assumptions

- The architecture (Lambda, Glue, S3) is scalable and can handle increased data volumes if necessary.
- The transformation process from **JSON** to **Parquet** was done to improve performance, reduce storage costs, and ensure the data is in a format optimized for future analysis and querying.

## 9. Future Improvements

- **Athena Integration**: In the future, use **AWS Athena** to query the Gold layer data directly from S3 for further analysis and reporting.
- **Tableau Integration**: The processed F1 data can be integrated with **Tableau** for visualizations and dashboards to provide interactive insights into the F1 race data.
- **Data Integrity**:  While the F1DataTransformation and F1_Statistics_Job jobs handle basic transformations, the Data Quality function in AWS Glue Jobs could be used for more advanced data validation, such as checking for missing values, duplicates, or inconsistencies. However, due to the limitations of using a free version of AWS Glue, this feature was not utilized in this project. Future improvements could include integrating Data Quality to ensure better data integrity and validation during the ETL process.

## 10. Architecture Overview
This data pipeline architecture uses a combination of AWS services to efficiently ingest, process, store, and analyze F1 race data. The pipeline involves several stages:

1. **Data Ingestion**: Data is retrieved from the **F1 API**, which serves as the primary data source.
2. **AWS Lambda**: The data is ingested into **AWS Lambda** for processing before being stored in **Amazon S3**.
3. **Data Storage**: The raw data is stored in **S3 Raw Data**. 
4. **Data Processing**: **AWS Glue** is used for transforming the Raw data data, first into a cleaned state (Silver) and then into a simplified, ready-for-analysis format (Gold). This data is cleaned and processed into **S3 Silver Data** and **S3 Gold Data** using **AWS Glue Jobs**.
5. **Data Consumption**: The final data, stored in **S3 Gold Data** and  **S3 Silver Data**, is queried using **AWS Athena**. The results are then visualized and analyzed using **Analytics System** for insights and reporting.

- You can see the results under `Data Architecture Design.png ` 
