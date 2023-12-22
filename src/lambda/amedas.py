import uuid
from logging import getLogger
from urllib.parse import unquote_plus

import boto3
from preprocessing.amedas import load_amedas_data

logger = getLogger(__file__)
s3_client = boto3.client("s3")


def lambda_handler(event, context):
    for record in event["Records"]:
        bucket = record["s3"]["bucket"]["name"]
        key = unquote_plus(record["s3"]["object"]["key"])
        tmpkey = key.replace("/", "")

        unique_id = uuid.uuid4()
        download_path = f"/tmp/{unique_id}_{tmpkey}"
        upload_path = f"/tmp/{unique_id}_{tmpkey}_processed"

        s3_client.download_file(bucket, key, download_path)

        try:
            df = load_amedas_data(download_path)
            df.to_csv(upload_path, index=False)
        except Exception as e:
            logger.error(f"Could not convert {key}: {e}")
            return

        s3_client.upload_file(upload_path, f"{bucket}-processed", key)
