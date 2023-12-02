from logging import getLogger
from pathlib import Path

import polars as pl
from agg import aggregate_minutely
from circling import compute_heading_transition, detect_circling
from igc import igc2csv
from tqdm import tqdm

ROOT = Path(__file__).parents[2]
logger = getLogger(__file__)

if __name__ == "__main__":
    source_dir = ROOT / "data" / "igc"
    target_dir = ROOT / "data" / "csv"
    target_dir_agg = ROOT / "data" / "agg"

    for path in tqdm(list(source_dir.glob("*.igc"))):
        filename = path.stem

        target_path = target_dir / f"{filename}.csv"
        # if target_path.exists():
        #     continue
        try:
            df = igc2csv(path)
            df["heading"] = compute_heading_transition(df["latitude"], df["longitude"])
            df["circling"] = detect_circling(df["heading"])
            df.to_csv(target_path, index=False)
        except Exception:
            logger.error(f"Could not convert {filename}.igc to csv.")

        target_path_agg = target_dir_agg / f"{filename}.csv"
        # if target_dir_agg.exists():
        #     continue
        try:
            df = pl.from_pandas(df)
            df_agg = aggregate_minutely(df).filter(pl.col("circling") == 1)
            df_agg.write_csv(target_path_agg)
        except Exception:
            logger.error(f"Could not aggregate {filename}.csv")
