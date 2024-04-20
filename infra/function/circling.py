import math

import pandas as pd


def _calc_bearing(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    2点間の方位角を求める
    """
    # 緯度経度をラジアンに変換
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

    # 方位角を計算
    delta_lon = lon2 - lon1
    x = math.sin(delta_lon) * math.cos(lat2)
    y = math.cos(lat1) * math.sin(lat2) - math.sin(lat1) * math.cos(lat2) * math.cos(
        delta_lon
    )
    bearing = math.atan2(x, y)

    # ラジアンを度に変換し、方位角を0～360度の範囲に調整
    bearing = math.degrees(bearing)
    bearing = (bearing + 360) % 360

    return bearing


def _filter_short_sequence(sr: pd.Series, min_length: int) -> pd.Series:
    """
    0または1からなる系列に対し、1が連続する回数が指定した回数よりも少ない場合、それを0に変換する
    """
    groups = sr.diff().ne(0).cumsum()
    group_lengths = sr.groupby(groups).transform("size")
    return sr.where((sr == 0) | (group_lengths >= min_length), other=0)


def compute_heading_transition(lats: pd.Series, lons: pd.Series) -> pd.Series:
    """
    緯度と経度の時系列変化を受け取り、ヘディングの推移を出力する
    """
    coodinates = pd.DataFrame({"latitude": lats, "longitude": lons})

    def func(sr, df):
        df_sub = df.loc[sr.index, ["latitude", "longitude"]]
        return _calc_bearing(
            df_sub.iloc[0, 0],
            df_sub.iloc[0, 1],
            df_sub.iloc[1, 0],
            df_sub.iloc[1, 1],
        )

    # https://qiita.com/matsxxx/items/49068d2cf0c3311819dd
    heading_transition = (
        coodinates["latitude"]
        .rolling(window=2, min_periods=2)
        .apply(func, args=(coodinates,))
    )

    return heading_transition


def detect_circling(
    headings: pd.Series, min_angle: int = 5, min_duration: int = 50
) -> pd.Series:
    """
    ヘディングの推移から連続旋回を検出する
    """
    # ヘディングの変化量がmin_angleよりも大きい場合にフラグを立てる
    headings_diff = headings.diff().abs().apply(lambda x: min(x, 360 - x))
    circling = headings_diff.ge(min_angle).astype(int)

    # 継続時間が短いものは検出しない
    circling = _filter_short_sequence(circling, min_length=min_duration)

    return circling
