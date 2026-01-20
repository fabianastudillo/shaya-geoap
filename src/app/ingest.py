"""Data ingestion utilities for loading data.json into PostGIS."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable

from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncEngine

from app.models import AccessPoint


def _parse_points(data: dict) -> Iterable[dict]:
    """Flatten nested JSON structure into rows ready for DB insertion."""

    for campus, buildings in data.items():
        for building, floors in buildings.items():
            for floor, floor_data in floors.items():
                puntos = floor_data.get("Puntos", {})
                for ap_code, info in puntos.items():
                    coords = info.get("coordenadas")
                    if not coords:
                        continue
                    lat = coords.get("lat")
                    lon = coords.get("lon")
                    alt = coords.get("alt")
                    if lat is None or lon is None:
                        continue
                    yield {
                        "ap_code": ap_code,
                        "campus": campus,
                        "building": building,
                        "floor": floor,
                        "status": info.get("status"),
                        "reference": info.get("referencia"),
                        "altitude_m": alt,
                        "location": f"SRID=4326;POINTZ({lon} {lat} {alt if alt is not None else 0})",
                    }


def load_data(engine: AsyncEngine, json_path: Path) -> int:
    """Load JSON data into PostGIS, skipping duplicates by ap_code.

    Returns number of inserted or updated rows.
    """

    content = json.loads(json_path.read_text(encoding="utf-8"))
    rows = list(_parse_points(content))
    if not rows:
        return 0

    stmt = (
        insert(AccessPoint)
        .values(rows)
        .on_conflict_do_update(
            index_elements=[AccessPoint.ap_code],
            set_={
                "status": insert(AccessPoint).excluded.status,
                "reference": insert(AccessPoint).excluded.reference,
                "campus": insert(AccessPoint).excluded.campus,
                "building": insert(AccessPoint).excluded.building,
                "floor": insert(AccessPoint).excluded.floor,
                "altitude_m": insert(AccessPoint).excluded.altitude_m,
                "location": insert(AccessPoint).excluded.location,
            },
        )
    )

    async def _execute() -> int:
        async with engine.begin() as conn:
            result = await conn.execute(stmt)
            return result.rowcount or 0

    import asyncio

    return asyncio.run(_execute())
