import datetime
from typing import Optional

import pandas as pd
from amedas_scraper.scraper import get_amedas_data
from google.cloud import bigquery
from prefect import flow, task

# point code
PREC_NO = "42"  # 群馬県
BLOCK_NO = "0354"  # 館林

# decorate imported function
get_amedas_data = task(get_amedas_data)


@task
def output_to_bq(
    df: pd.DataFrame, dataset_id: str, table_id: str, project: Optional[str] = None
) -> None:
    """
    データフレームをBigQueryの指定したテーブルに追加する
    """
    client = bigquery.Client(project)
    table = client.dataset(dataset_id).table(table_id)

    job_config = bigquery.LoadJobConfig()
    job_config.autodetect = True
    job_config.write_disposition = bigquery.WriteDisposition.WRITE_APPEND

    job = client.load_table_from_dataframe(df, table, job_config=job_config)
    job.result()

    return


@flow
def load_weather_data_to_bq():
    """
    アメダスデータをスクレイピングしてBigQueryに読み込む
    """
    yesterday = datetime.date.today() - datetime.timedelta(days=1)
    df = get_amedas_data(prec_no=PREC_NO, block_no=BLOCK_NO, date=yesterday)
    output_to_bq(df, dataset_id="data_lake", table_id="amedas", project="glider-dash")


if __name__ == "__main__":
    load_weather_data_to_bq()
