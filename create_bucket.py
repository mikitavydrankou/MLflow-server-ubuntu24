import os
import boto3
from dotenv import load_dotenv

load_dotenv()

endpoint = os.getenv("MLFLOW_S3_ENDPOINT_URL")
access_key = os.getenv("AWS_ACCESS_KEY_ID")
secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
bucket_name = os.getenv("MLFLOW_BUCKET_NAME")

def check_bucket_access():
    s3 = boto3.client(
        "s3",
        endpoint_url=endpoint,
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
    )
    try:
        s3.head_bucket(Bucket=bucket_name)
        print(f"[OK] Bucket '{bucket_name}' available.")
    except Exception as e:
        print(f"[ERROR] No access to bucket '{bucket_name}': {e}")

if __name__ == "__main__":
    check_bucket_access()
