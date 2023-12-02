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
