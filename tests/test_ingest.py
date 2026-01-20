import json
from pathlib import Path

import pytest

from app.ingest import _parse_points


@pytest.fixture()
def sample_data(tmp_path: Path) -> Path:
    payload = {
        "Campus": {
            "Building": {
                "0": {
                    "Puntos": {
                        "AP-1": {
                            "status": "up",
                            "referencia": "Ref",
                            "coordenadas": {"lat": 1.0, "lon": 2.0, "alt": 3},
                        }
                    }
                }
            }
        }
    }
    json_path = tmp_path / "data.json"
    json_path.write_text(json.dumps(payload), encoding="utf-8")
    return json_path


def test_parse_points_returns_rows(sample_data: Path) -> None:
    data = json.loads(sample_data.read_text(encoding="utf-8"))
    rows = list(_parse_points(data))
    assert len(rows) == 1
    row = rows[0]
    assert row["ap_code"] == "AP-1"
    assert row["campus"] == "Campus"
    assert row["building"] == "Building"
    assert row["floor"] == "0"
    assert row["location"].startswith("SRID=4326;POINTZ(")


def test_parse_points_skips_missing_coords() -> None:
    data = {"Campus": {"Building": {"0": {"Puntos": {"AP-1": {"status": "up"}}}}}}
    rows = list(_parse_points(data))
    assert rows == []


def test_parse_points_skips_null_lat_lon() -> None:
    data = {
        "Campus": {
            "Building": {
                "0": {
                    "Puntos": {
                        "AP-1": {
                            "status": "up",
                            "coordenadas": {"lat": None, "lon": 2.0, "alt": 3},
                        }
                    }
                }
            }
        }
    }
    rows = list(_parse_points(data))
    assert rows == []
