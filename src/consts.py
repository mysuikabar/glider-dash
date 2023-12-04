from pathlib import Path

ROOT = Path(__file__).parents[1]
LOG_DATA_DIR = ROOT / "data" / "log"
AMEDAS_DATA_DIR = ROOT / "data" / "amedas"

TMP_DIR = Path("/tmp/uploads")

MAP_CENTER = {"lon": 139.41889, "lat": 36.21139}  # 妻沼の座標
