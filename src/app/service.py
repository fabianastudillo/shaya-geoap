"""Service layer for access point operations."""
from collections.abc import Sequence

from sqlalchemy.ext.asyncio import AsyncSession

from app.config import get_settings
from app.repositories import AccessPointRepository
from app.schemas import AccessPointDetail, AccessPointNearest

_settings = get_settings()


class AccessPointService:
    """Business logic for access points."""

    def __init__(self, session: AsyncSession):
        self._session = session

    async def nearest(
        self, ap_code: str, limit: int | None = None, max_distance_m: float | None = None
    ) -> Sequence[AccessPointNearest]:
        resolved_limit = limit or _settings.default_nearest_limit
        resolved_max_distance = max_distance_m or _settings.default_max_distance_m
        return await AccessPointRepository.list_nearest(
            session=self._session,
            ap_code=ap_code,
            limit=resolved_limit,
            max_distance_m=resolved_max_distance,
        )

    async def location(self, ap_code: str) -> AccessPointDetail | None:
        return await AccessPointRepository.get_location(self._session, ap_code)
