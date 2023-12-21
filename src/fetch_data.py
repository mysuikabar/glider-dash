from pathlib import Path

import boto3


def fetch_csv_from_s3(bucket_name: str, s3_folder: str, local_dir: Path):
    """
    S3上の指定したフォルダのcsvファイルをローカルにダウンロードする
    """
    if not local_dir.exists():
        local_dir.mkdir(parents=True)

    s3 = boto3.resource("s3")
    bucket = s3.Bucket(bucket_name)

    for obj in bucket.objects.filter(Prefix=s3_folder):
        if obj.key.endswith(".csv"):
            file_path = local_dir / obj.key.split("/")[-1]

            if file_path.exists():
                continue
            else:
                bucket.download_file(obj.key, file_path)
