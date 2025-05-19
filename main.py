import subprocess
import os
from pathlib import Path
import psycopg2
import boto3
from dotenv import load_dotenv

def execute_command(command):
    print(f"\n[RUN] {command}")
    subprocess.run(command, shell=True, check=True)

VENV_DIR = Path("venv")
PYTHON = VENV_DIR / "bin" / "python"
PIP = VENV_DIR / "bin" / "pip"

commands_to_execute = [
    "curl -fsSL https://get.docker.com -o get-docker.sh",
    "sudo sh get-docker.sh",
    "sudo docker compose up -d --build",
    "sudo apt update",
    "sudo apt install -y python3-venv",
    f"python3 -m venv {VENV_DIR}",
    f"{PIP} install --upgrade pip",
    f"{PIP} install boto3 python-dotenv mlflow scikit-learn psycopg2-binary",
    f"{PYTHON} create_bucket.py"
]

def test_s3_connection():
    print("\n[TEST] Check connection to DigitalOcean Spaces (S3)...")
    load_dotenv()
    bucket_name = os.getenv("MLFLOW_BUCKET_NAME")

    try:
        s3 = boto3.client(
            "s3",
            endpoint_url=os.getenv("MLFLOW_S3_ENDPOINT_URL"),
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        )
        s3.head_bucket(Bucket=bucket_name)
        print(f"[OK] Access to bucket '{bucket_name}' approved.")
    except Exception as e:
        print("[ERROR] Connection failed to S3:", e)

def test_postgres_connection():
    print("\n[TEST] Check connection to PostgreSQL...")
    import psycopg2
    from dotenv import load_dotenv
    load_dotenv()

    try:
        conn = psycopg2.connect(
            host="localhost",
            port=5423,           
            user=os.environ["PG_USER"],
            password=os.environ["PG_PASSWORD"],
            dbname=os.environ["PG_DATABASE"]
        )
        print("[OK] Success connection to PostgreSQL")
        conn.close()
    except Exception as e:
        print("[ERROR] Connection error PostgreSQL:", e)

if __name__ == "__main__":
    for cmd in commands_to_execute:
        try:
            execute_command(cmd)
        except subprocess.CalledProcessError as e:
            print(f"[ERROR] Error via: {e.cmd}")
            exit(1)
    test_s3_connection()
    test_postgres_connection()
