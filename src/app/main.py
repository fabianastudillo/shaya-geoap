"""FastAPI application exposing nearest access point queries."""
from fastapi import Depends, FastAPI, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_session
from app.schemas import AccessPointNearest
from app.service import AccessPointService

app = FastAPI(title="GeoAP", version="0.1.0")


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/aps/{ap_code}/nearest", response_model=list[AccessPointNearest])
async def get_nearest_aps(
    ap_code: str,
    limit: int = Query(default=None, ge=1, le=200, description="Max number of results"),
    max_distance_m: float | None = Query(
        default=None, ge=0, description="Maximum distance in meters to include"
    ),
    session: AsyncSession = Depends(get_session),
) -> list[AccessPointNearest]:
    service = AccessPointService(session)
    results = await service.nearest(ap_code=ap_code, limit=limit, max_distance_m=max_distance_m)
    if not results:
        raise HTTPException(status_code=404, detail="Access point not found or no neighbors")
    return list(results)
