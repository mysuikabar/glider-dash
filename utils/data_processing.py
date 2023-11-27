import datetime
import re
from logging import getLogger
from pathlib import Path

import pandas as pd
from tqdm import tqdm

logger = getLogger(__file__)


def igc2csv(path: Path) -> pd.DataFrame:
    """
    igcファイルをcsvに変換する。
    神記事のコードをもとに一部修正: https://mtkbirdman.com/python-convert-igc-file-to-csv-data
    """
    with open(path) as f:
        igcfile = f.readlines()
    igcfile = [line.rstrip("\n") for line in igcfile]

    # Extract flight date
    for line in igcfile:
        if result := re.fullmatch(
            r"HFDTE(?P<day>\d{2})(?P<month>\d{2})(?P<year>\d{2})", line
        ):
            date = datetime.date(
                int("20" + result.group("year")),
                int(result.group("month")),
                int(result.group("day")),
            )
            break

    # Extract B-record from IGC file
    igc_B = [
        [igcfile.index(lines), lines]
        for lines in igcfile
        if "B" in lines[0]
        if "A" in lines
    ]
    list_B = [
        [
            lines[0],
            lines[1][0],
            lines[1][1:7],
            lines[1][7:14],
            lines[1][14],
            lines[1][15:23],
            lines[1][23],
            lines[1][24],
            lines[1][25:30],
            lines[1][30:],
        ]
        for lines in igc_B
    ]

    # Convert text of B-record to values
    idx = 0
    for _ in list_B:
        list_B[idx][2] = datetime.datetime(
            date.year,
            date.month,
            date.day,
            int(list_B[idx][2][:2]),
            int(list_B[idx][2][2:4]),
            int(list_B[idx][2][4:]),
        )
        list_B[idx][3] = float(list_B[idx][3]) / 100000.0
        list_B[idx][5] = float(list_B[idx][5]) / 100000.0
        list_B[idx][8] = float(list_B[idx][8])
        list_B[idx][9] = float(list_B[idx][9])
        idx += 1

    # Create dataframe from list of records and export it as CSV file
    df_B = pd.DataFrame(
        list_B,
        columns=[
            "igc_index",
            "record_type",
            "UTC_time",
            "latitude",
            "NS",
            "longitude",
            "EW",
            "fix_validity",
            "press_alt",
            "GNSS_alt",
        ],
    )

    return df_B


if __name__ == "__main__":
    source_dir = Path(__file__).parents[1] / "data/igc"
    target_dir = Path(__file__).parents[1] / "data/csv"

    for path in tqdm(list(source_dir.glob("*.igc"))):
        target_path = target_dir / path.with_suffix(".csv").name
        if target_path.exists():
            continue

        try:
            igc2csv(path).to_csv(target_path, index=False)
        except:
            logger.error(f"Could not convert {path.name} to csv.")
