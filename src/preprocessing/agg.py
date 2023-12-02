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


def load_and_concat_csv(source_dir: Path) -> pd.DataFrame:
    """
    指定したディレクトリの直下にあるcsvファイルを全て読み込んで結合する
    """
    df_list = [pd.read_csv(path) for path in source_dir.glob("*.csv")]
    return pd.concat(df_list, ignore_index=True)
