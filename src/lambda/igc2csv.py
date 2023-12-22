import uuid
from logging import getLogger
from pathlib import Path
from urllib.parse import unquote_plus

import boto3
from preprocessing.circling import compute_heading_transition, detect_circling
from preprocessing.igc import igc2csv

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
            df = igc2csv(download_path)
            df["heading"] = compute_heading_transition(df["latitude"], df["longitude"])
            df["circling"] = detect_circling(df["heading"])
            df.to_csv(upload_path, index=False)
        except Exception as e:
            logger.error(f"Could not convert {key}: {e}")
            return

        s3_client.upload_file(
            upload_path, f"{bucket}-processed", str(Path(key).with_suffix(".csv"))
        )
