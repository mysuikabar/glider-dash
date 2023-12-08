from pathlib import Path

import pandas as pd


def _direction_to_angle(direction: str) -> float:
    """
    16方位を角度に変換する
    """
    directions = {
        "北": 0,
        "北北東": 22.5,
        "北東": 45,
        "東北東": 67.5,
        "東": 90,
        "東南東": 112.5,
        "南東": 135,
        "南南東": 157.5,
        "南": 180,
        "南南西": 202.5,
        "南西": 225,
        "西南西": 247.5,
        "西": 270,
        "西北西": 292.5,
        "北西": 315,
        "北北西": 337.5,
    }
    return directions.get(direction, 0)  # 16方位以外は0に割り当てる（ex. 静穏）


def load_amedas_data(path: Path) -> pd.DataFrame:
    """
    アメダスデータをフォーマットを整えてロードする
    https://www.data.jma.go.jp/gmd/risk/obsdl/
    """
    df = pd.read_csv(path, encoding="shift-jis", skiprows=[0, 1, 2, 4, 5])

    column_mapper = {
        "年月日時": "timestamp",
        "気温(℃)": "temperature",
        "風速(m/s)": "wind speed",
        "風速(m/s).1": "wind direction",
        "相対湿度(％)": "humidity",
        "露点温度(℃)": "dew point",
        "日照時間(時間)": "daylight hours",
        "現地気圧(hPa)": "pressure",
        "視程(km)": "visibility",
    }
    df = df.filter(list(column_mapper.keys()), axis="columns").rename(
        column_mapper, axis="columns"
    )
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["wind direction"] = df["wind direction"].map(_direction_to_angle)

    return df
