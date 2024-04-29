import numpy as np
from amedas_scraper.scraper import get_amedas_data


def test_run():
    df = get_amedas_data(prec_no="42", block_no="0354", year=2024, month=1, day=1)

    columns_expected = [
        "timestamp",
        "rainfall",
        "temperature",
        "humidity",
        "wind_speed",
        "wind_direction",
        "wind_speed_max",
        "wind_direction_max",
        "daylight_hours",
    ]

    assert list(df.columns) == columns_expected
    for col in columns_expected:
        if col != "timestamp":
            assert df[col].dtype == np.float64
