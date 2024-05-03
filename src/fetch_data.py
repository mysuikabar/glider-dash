from pathlib import Path

import boto3


def fetch_csv_from_s3(bucket_name: str, local_dir: Path, s3_folder: str = ""):
    """
    S3上の指定したフォルダのcsvファイルをローカルにダウンロードする
    """
    s3 = boto3.resource("s3")
    bucket = s3.Bucket(bucket_name)

    for obj in bucket.objects.filter(Prefix=s3_folder):
        if obj.key.endswith(".csv"):
            file_path = local_dir / obj.key

            if file_path.exists():
                continue
            else:
                file_path.parent.mkdir(parents=True, exist_ok=True)
                bucket.download_file(obj.key, file_path)
