import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List

import pandas as pd


def _convert_dms_to_decimal(value: float) -> float:
    """
    緯度経度の60進法を10進法に変換する
    """
    integer_part = int(value)
    decimal_part_dms = value - integer_part

    decimal_part_dec = decimal_part_dms * 100 / 60

    return integer_part + decimal_part_dec


def igc2csv(path: Path) -> pd.DataFrame:
    """
    igcファイルをcsvに変換する
    """
    with open(path) as f:
        content = f.readlines()
    lines = [line.rstrip("\n") for line in content]

    # extract date
    h_record_pattern = r"HFDTE(\d{2})(\d{2})(\d{2})"  # HFDTE day month year

    for line in lines:
        if result := re.fullmatch(h_record_pattern, line):
            day = int(result.group(1))
            month = int(result.group(2))
            year = int("20" + result.group(3))
            break

    data: Dict[str, List] = {}
    data["timestamp"] = []
    data["latitude"] = []
    data["longitude"] = []
    data["altitude(press)"] = []
    data["altitude(gnss)"] = []

    # extract B-record
    b_record_pattern = r"B(\d{6})(\d{7})N(\d{8})EA(-\d{4}|\d{5})(-\d{4}|\d{5})"  # B time lat lon A PressAlt GNSSAlt

    for line in lines:
        if result := re.match(b_record_pattern, line):
            # timestamp
            hhmmss = result.group(1)
            timestamp = datetime(
                year, month, day, int(hhmmss[:2]), int(hhmmss[2:4]), int(hhmmss[4:])
            )
            data["timestamp"].append(timestamp)

            # latitude and longitude
            latitude = float(result.group(2)) / 100000
            latitude = _convert_dms_to_decimal(latitude)
            longitude = float(result.group(3)) / 100000
            longitude = _convert_dms_to_decimal(longitude)
            data["latitude"].append(latitude)
            data["longitude"].append(longitude)

            # altitude
            alt_press = int(result.group(4))
            alt_gnss = int(result.group(5))
            data["altitude(press)"].append(alt_press)
            data["altitude(gnss)"].append(alt_gnss)

    df = pd.DataFrame(data=data)

    # change time zone
    df["timestamp"] = df["timestamp"].dt.tz_localize("UTC")
    df["timestamp"] = df["timestamp"].dt.tz_convert("Asia/Tokyo")
    df["timestamp"] = df["timestamp"].dt.tz_localize(None)

    return df
