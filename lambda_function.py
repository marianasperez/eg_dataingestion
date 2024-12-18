import json
import urllib.request
import boto3
from datetime import datetime

def lambda_handler(event, context):
    # API URL with the API key
    api_key = 'CwnyRqJ1zr7zpX6Y4VIa5TgoT9OAa5anRuPi3ORP'
    url = f"https://api.sportradar.com/formula1/trial/v2/en/sport_events/sr%3Astage%3A1107547/probabilities.json?api_key={api_key}"

    # Send the GET request using urllib
    req = urllib.request.Request(url, headers={"accept": "application/json"})
    with urllib.request.urlopen(req) as response:
        data = json.load(response)

    # Upload the data to your S3 bucket
    s3 = boto3.client('s3')
    current_date = datetime.now().strftime('%Y-%m-%d')
    file_name = f"f1_data_{current_date}.json"
    s3_bucket = 'my-f1-data-bucket'  # Use your S3 bucket name here

    # Upload the data to S3
    s3.put_object(Bucket=s3_bucket, Key=file_name, Body=json.dumps(data))
    print(f"Data uploaded successfully to {s3_bucket}/{file_name}")
