import datetime
import re
from typing import Any, Dict, List, Optional

import pandas as pd


def _convert_dms_to_decimal(value: float) -> float:
    """
    緯度経度の60進法を10進法に変換する
    """
    integer_part = int(value)
    decimal_part_dms = value - integer_part
    decimal_part_dec = decimal_part_dms * 100 / 60

    return integer_part + decimal_part_dec


def _parse_b_record(line: str) -> Optional[Dict[str, Any]]:
    """
    igcファイルのB recordに含まれる時刻、緯度経度、高度の情報をパースする
    """
    pattern = r"B(\d{6})(\d{7})N(\d{8})EA(-\d{4}|\d{5})(-\d{4}|\d{5})"  # B hhmmss lat lon A PressAlt GNSSAlt
    result = re.match(pattern, line)

    if result is None:
        return None

    output: Dict[str, Any] = {}

    # time
    hhmmss = result.group(1)
    hour = int(hhmmss[:2])
    minute = int(hhmmss[2:4])
    second = int(hhmmss[4:])
    output["time"] = datetime.time(hour, minute, second)

    # latitulde, longitude
    latitude = float(result.group(2)) / 100000
    output["latitude"] = _convert_dms_to_decimal(latitude)
    longitude = float(result.group(3)) / 100000
    output["longitude"] = _convert_dms_to_decimal(longitude)

    # altitude
    output["altitude_press"] = int(result.group(4))
    output["altitude_gnss"] = int(result.group(5))

    return output


def _parse_date(line: str) -> Optional[datetime.date]:
    """
    igcファイルのH recordに含まれる日付の情報をパースする
    """
    pattern = r"HFDTE(\d{2})(\d{2})(\d{2})"  # HFDTE day month year
    result = re.fullmatch(pattern, line)

    if result is None:
        return None

    day = int(result.group(1))
    month = int(result.group(2))
    year = int("20" + result.group(3))

    return datetime.date(year, month, day)


def _parse_pilot(line: str) -> Optional[str]:
    """
    igcファイルのH recordに含まれるパイロットの情報をパースする
    """
    result = re.match(r"HFPLTPILOTINCHARGE:(.*)", line)
    return result.group(1) if result else None


def _parse_glider_type(line: str) -> Optional[str]:
    """
    igcファイルのH recordに含まれるグライダー型式の情報をパースする
    """
    result = re.match(r"HFGTYGLIDERTYPE:(.*)", line)
    return result.group(1) if result else None


def _parse_glider_id(line: str) -> Optional[str]:
    """
    igcファイルのH recordに含まれるグライダーIDの情報をパースする
    """
    result = re.match(r"HFGIDGLIDERID:(.*)", line)
    return result.group(1) if result else None


def igc2df(text: str) -> pd.DataFrame:
    """
    igcファイルをcsvに変換する
    """
    lines = [line.rstrip("\n") for line in text.splitlines()]

    # extract H record
    pilot, glider_type, glider_id = None, None, None
    for line in lines:
        if _parse_date(line):
            date = _parse_date(line)
        elif _parse_pilot(line):
            pilot = _parse_pilot(line)
        elif _parse_glider_type(line):
            glider_type = _parse_glider_type(line)
        elif _parse_glider_id(line):
            glider_id = _parse_glider_id(line)

    # extract B record
    data: Dict[str, List] = {}
    data["timestamp"] = []
    data["latitude"] = []
    data["longitude"] = []
    data["altitude"] = []
    data["altitude_gnss"] = []

    for line in lines:
        result = _parse_b_record(line)
        if result is None:
            continue

        timestamp = datetime.datetime.combine(date, result["time"])  # type: ignore
        data["timestamp"].append(timestamp)
        data["latitude"].append(result["latitude"])
        data["longitude"].append(result["longitude"])
        data["altitude"].append(result["altitude_press"])
        data["altitude_gnss"].append(result["altitude_gnss"])

    df = pd.DataFrame(data=data).assign(
        pilot=pilot, glider_type=glider_type, glider_id=glider_id
    )

    # change time zone
    df["timestamp"] = df["timestamp"].dt.tz_localize("UTC")
    df["timestamp"] = df["timestamp"].dt.tz_convert("Asia/Tokyo")
    df["timestamp"] = df["timestamp"].dt.tz_localize(None)

    return df
