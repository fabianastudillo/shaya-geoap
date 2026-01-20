#!/usr/bin/env python3
"""One-off loader to ingest data.json into PostGIS."""
from __future__ import annotations

import asyncio
import logging
from pathlib import Path

from sqlalchemy.ext.asyncio import create_async_engine

from app.config import get_settings
from app.ingest import load_data

logging.basicConfig(level=logging.INFO, format="%(levelname)s:%(message)s")


def main() -> None:
    settings = get_settings()
    engine = create_async_engine(settings.database_url, echo=False, pool_pre_ping=True)
    inserted = load_data(engine, Path("data.json"))
    logging.info("Upserted %s access points", inserted)
    # Async engine will be cleaned up on process exit; explicit dispose not needed here.


if __name__ == "__main__":
    main()
