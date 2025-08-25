import os
import boto3
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get AWS credentials and bucket info from environment variables
aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
aws_s3_bucket = os.getenv("AWS_S3_BUCKET")
aws_region = os.getenv("AWS_REGION")

# Check if all required environment variables are set
if not all([aws_access_key_id, aws_secret_access_key, aws_s3_bucket, aws_region]):
    print("Error: Missing required environment variables.")
    print("Please ensure AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_S3_BUCKET, and AWS_REGION are set in your .env file.")
else:
    # Create an S3 client
    s3_client = boto3.client(
        "s3",
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=aws_region
    )

    try:
        # List objects in the bucket
        print(f"Listing objects in bucket: {aws_s3_bucket}")
        response = s3_client.list_objects_v2(Bucket=aws_s3_bucket)

        if "Contents" in response:
            print("Objects found:")
            for obj in response["Contents"]:
                print(f"- {obj['Key']}")
        else:
            print("No objects found in the bucket.")

    except Exception as e:
        print(f"An error occurred: {e}")
