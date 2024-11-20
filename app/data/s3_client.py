import boto3
from botocore.config import Config
from botocore.exceptions import ClientError
from botocore import UNSIGNED

# TODO: Use a singleton client to avoid creating a new client for each request
def get_s3_client():
    return boto3.client('s3', config=Config(signature_version=UNSIGNED))


# TODO: Add retry logic
# TODO: Process data in batches
def get_s3_object(bucket_name, key):
    s3 = get_s3_client()
    try:
        response = s3.get_object(Bucket=bucket_name, Key=key)
        return response['Body']
    except ClientError as e:
        print(f"Error fetching object {key} from bucket {bucket_name}: {e}")
        return None
