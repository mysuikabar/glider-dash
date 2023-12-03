from pathlib import Path

import pandas as pd
import polars as pl


def aggregate_minutely(df: pl.DataFrame) -> pl.DataFrame:
    """
    ログデータを1分単位に集計する
    - 緯度、経度、高度の平均
    - 平均上昇率
    - 連続旋回フラグ
    """
    df_agg = (
        df.group_by_dynamic(pl.col("timestamp").set_sorted(), every="1m")
        .agg(
            pl.col("latitude").mean(),
            pl.col("longitude").mean(),
            pl.col("altitude(press)").mean(),
            pl.col("circling").min(),
            (
                pl.col("altitude(press)").last() - pl.col("altitude(press)").first()
            ).alias("alt_diff"),
            (pl.col("timestamp").last() - pl.col("timestamp").first()).alias(
                "time_diff"
            ),
        )
        .with_columns(
            (pl.col("alt_diff") / pl.col("time_diff").dt.total_seconds()).alias(
                "climb_rate"
            )
        )
        .drop(["alt_diff", "time_diff"])
    )

    return df_agg


def load_and_concat_csv(source_dir: Path) -> pl.DataFrame:
    """
    指定したディレクトリの直下にあるcsvファイルを全て読み込んで結合する
    """
    df_list = [pd.read_csv(path) for path in source_dir.glob("*.csv")]
    df = pd.concat(df_list, ignore_index=True)
    return pl.from_pandas(df)


def merge_log_and_amedas_data(
    df_log: pl.DataFrame, df_amedas: pl.DataFrame
) -> pl.DataFrame:
    """
    ログデータとアメダスデータを結合する
    """
    df = df_log.with_columns(
        pl.col("timestamp").dt.round("1h").alias("timestamp_round")
    ).join(df_amedas, left_on="timestamp_round", right_on="timestamp", how="left")

    return df
