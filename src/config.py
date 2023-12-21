from dataclasses import dataclass
from pathlib import Path

from .consts import ROOT


@dataclass
class Config:
    tmp_dir = Path(
        "/tmp/uploads"
    )  # アップロードされたIGCファイルを保存する一時ディレクトリ
    log_data_dir = ROOT / "data" / "log"  # ログデータを保存するディレクトリ
    amedas_data_dir = ROOT / "data" / "amedas"  # アメダスデータを保存するディレクトリ
