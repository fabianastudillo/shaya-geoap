"""Database models."""
from datetime import datetime

from geoalchemy2 import Geography
from sqlalchemy import DateTime, Float, String, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """Base declarative class."""


class AccessPoint(Base):
    """Wireless access point metadata and geospatial position."""

    __tablename__ = "access_points"

    id: Mapped[int] = mapped_column(primary_key=True)
    ap_code: Mapped[str] = mapped_column(String, unique=True, nullable=False, index=True)
    campus: Mapped[str] = mapped_column(String, nullable=False)
    building: Mapped[str] = mapped_column(String, nullable=False)
    floor: Mapped[str] = mapped_column(String, nullable=False)
    status: Mapped[str | None] = mapped_column(String, nullable=True)
    reference: Mapped[str | None] = mapped_column(String, nullable=True)
    altitude_m: Mapped[float | None] = mapped_column(Float, nullable=True)
    location: Mapped[str] = mapped_column(
        Geography(geometry_type="POINTZ", srid=4326), nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )
