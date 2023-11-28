from logging import getLogger
from pathlib import Path

from circling import compute_heading_transition, detect_circling
from igc import igc2csv
from tqdm import tqdm

logger = getLogger(__file__)

if __name__ == "__main__":
    source_dir = Path(__file__).parents[2] / "data/igc"
    target_dir = Path(__file__).parents[2] / "data/csv"

    for path in tqdm(list(source_dir.glob("*.igc"))):
        target_path = target_dir / path.with_suffix(".csv").name
        # if target_path.exists():
        #     continue

        try:
            df = igc2csv(path)
            df["heading"] = compute_heading_transition(df["latitude"], df["longitude"])
            df["circling"] = detect_circling(df["heading"])
            df.to_csv(target_path, index=False)
        except Exception:
            logger.error(f"Could not convert {path.name} to csv.")
