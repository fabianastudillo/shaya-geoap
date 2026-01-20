"""Repository helpers for access points."""
from collections.abc import Sequence
from typing import Any

from geoalchemy2 import Geometry
from sqlalchemy import Select, cast, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app import schemas
from app.models import AccessPoint


class AccessPointRepository:
    """Data access layer for access points."""

    @staticmethod
    async def get_by_code(session: AsyncSession, ap_code: str) -> AccessPoint | None:
        stmt = select(AccessPoint).where(AccessPoint.ap_code == ap_code)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()

    @staticmethod
    async def list_nearest(
        session: AsyncSession, ap_code: str, limit: int, max_distance_m: float | None
    ) -> Sequence[schemas.AccessPointNearest]:
        base_ap = await AccessPointRepository.get_by_code(session, ap_code)
        if base_ap is None:
            return []

        base_location_subq = (
            select(AccessPoint.location).where(AccessPoint.ap_code == ap_code).scalar_subquery()
        )

        distance_expr = func.ST_Distance(AccessPoint.location, base_location_subq)

        location_geom = cast(AccessPoint.location, Geometry(geometry_type="POINTZ", srid=4326))

        stmt: Select[Any] = (
            select(
                AccessPoint.ap_code,
                AccessPoint.status,
                AccessPoint.reference,
                AccessPoint.campus,
                AccessPoint.building,
                AccessPoint.floor,
                AccessPoint.altitude_m,
                func.ST_Y(location_geom).label("latitude"),
                func.ST_X(location_geom).label("longitude"),
                distance_expr.label("distance_m"),
            )
            .where(AccessPoint.ap_code != ap_code)
            .order_by(distance_expr)
            .limit(limit)
        )

        if max_distance_m is not None:
            stmt = stmt.where(distance_expr <= max_distance_m)

        result = await session.execute(stmt)
        rows = result.mappings().all()
        return [schemas.AccessPointNearest(**row) for row in rows]

    @staticmethod
    async def get_location(session: AsyncSession, ap_code: str) -> schemas.AccessPointDetail | None:
        location_geom = cast(AccessPoint.location, Geometry(geometry_type="POINTZ", srid=4326))

        stmt = select(
            AccessPoint.ap_code,
            AccessPoint.status,
            AccessPoint.reference,
            AccessPoint.campus,
            AccessPoint.building,
            AccessPoint.floor,
            AccessPoint.altitude_m,
            func.ST_Y(location_geom).label("latitude"),
            func.ST_X(location_geom).label("longitude"),
        ).where(AccessPoint.ap_code == ap_code)

        result = await session.execute(stmt)
        row = result.mappings().first()
        return schemas.AccessPointDetail(**row) if row else None
