import os
import pandas as pd
from datetime import datetime
import boto3
from botocore.exceptions import NoCredentialsError

def write_parquet(logs, output_dir="data/parquet_output"):
    """
    Writes logs to Parquet files partitioned by service and date.
    """
    if not logs:
        print("No logs to write.")
        return

    df = pd.DataFrame(logs)
    df['date'] = pd.to_datetime(df['timestamp']).dt.date

    for (service, date), group in df.groupby(['service', 'date']):
        path = os.path.join(output_dir, f"service={service}/date={date}")
        os.makedirs(path, exist_ok=True)
        file_path = os.path.join(path, "data.parquet")
        group.drop(columns=["date"]).to_parquet(file_path, index=False)
        print(f"Saved: {file_path}")

def upload_to_s3(local_dir, bucket_name, s3_prefix="observability/"):
    """
    Uploads all .parquet files in a directory to S3.
    """
    s3 = boto3.client('s3')

    for root, _, files in os.walk(local_dir):
        for file in files:
            if file.endswith(".parquet"):
                local_path = os.path.join(root, file)
                relative_path = os.path.relpath(local_path, local_dir)
                s3_key = os.path.join(s3_prefix, relative_path).replace("\\", "/")
                try:
                    s3.upload_file(local_path, bucket_name, s3_key)
                    print(f"Uploaded {s3_key} to s3://{bucket_name}/")
                except NoCredentialsError:
                    print("❌ AWS credentials not found.")
                    return
