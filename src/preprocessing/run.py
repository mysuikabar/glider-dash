from logging import INFO, getLogger
from pathlib import Path

import polars as pl
from agg import aggregate_minutely
from amedas import load_amedas_data
from circling import compute_heading_transition, detect_circling
from igc import igc2csv
from tqdm import tqdm

from src.config import Config

logger = getLogger(__file__)
logger.setLevel(INFO)


def convert_igc_to_csv(source_dir: Path, target_dir: Path):
    for path in tqdm(list(source_dir.glob("*.igc"))):
        filename = path.name
        target_path = (target_dir / filename).with_suffix(".csv")
        # if target_path.exists():
        #     continue

        try:
            df = igc2csv(path)
            df["heading"] = compute_heading_transition(df["latitude"], df["longitude"])
            df["circling"] = detect_circling(df["heading"])
            df.to_csv(target_path, index=False)
        except Exception:
            logger.error(f"Could not convert {filename}.igc to csv.")


def aggregate_log_data(source_dir: Path, target_dir: Path):
    for path in tqdm(list(source_dir.glob("*.csv"))):
        filename = path.name
        target_path = target_dir / filename
        # if target_path.exists():
        #     continue

        try:
            df = pl.read_csv(path).with_columns(
                pl.col("timestamp").str.strptime(pl.Datetime)
            )
            df_agg = aggregate_minutely(df).filter(pl.col("circling") == 1)
            df_agg.write_csv(target_path)
        except Exception:
            logger.error(f"Could not aggregate {filename}")


def processing_amedas_data(source_dir: Path, target_dir: Path):
    for path in tqdm(list(source_dir.glob("*.csv"))):
        filename = path.name
        target_path = target_dir / filename
        # if target_path.exists():
        #     continue

        try:
            df = load_amedas_data(path)
            df.to_csv(target_path, index=False)
        except Exception:
            logger.error(f"Could not aggregate {filename}.csv.")


if __name__ == "__main__":
    logger.info("Converting igc to csv...")
    convert_igc_to_csv(Config.log_data_dir / "igc", Config.log_data_dir / "csv")
    logger.info("Completed!")

    logger.info("Aggregating log data...")
    aggregate_log_data(Config.log_data_dir / "csv", Config.log_data_dir / "agg")
    logger.info("Completed!")

    logger.info("Processing amedas data...")
    processing_amedas_data(
        Config.amedas_data_dir / "raw", Config.amedas_data_dir / "processed"
    )
    logger.info("Completed!")
