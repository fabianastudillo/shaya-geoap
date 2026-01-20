"""Pydantic schemas for API payloads."""
from typing import Optional

from pydantic import BaseModel, Field


class AccessPointBase(BaseModel):
    ap_code: str = Field(..., description="Unique access point code")
    status: Optional[str] = Field(default=None, description="Operational status")
    reference: Optional[str] = Field(default=None, description="Human readable reference")
    campus: str = Field(..., description="Campus name")
    building: str = Field(..., description="Building name")
    floor: str = Field(..., description="Floor identifier")
    altitude_m: Optional[float] = Field(default=None, description="Altitude in meters")
    latitude: float = Field(..., description="Latitude in decimal degrees")
    longitude: float = Field(..., description="Longitude in decimal degrees")


class AccessPointNearest(AccessPointBase):
    distance_m: float = Field(..., description="Distance from origin in meters")

    model_config = {
        "json_schema_extra": {
            "example": {
                "ap_code": "BALZAY-AU1-PB-155",
                "status": "up",
                "reference": "ENTRADA AL EDIFICIO",
                "campus": "Balzay",
                "building": "Aulario1",
                "floor": "0",
                "altitude_m": 3,
                "latitude": -2.89175445,
                "longitude": -79.03696597,
                "distance_m": 12.5,
            }
        }
    }
