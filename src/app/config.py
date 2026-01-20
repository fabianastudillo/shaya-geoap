"""Application settings management."""
from functools import lru_cache
from typing import Optional

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Typed application configuration loaded from environment."""

    database_url: str = Field(..., alias="DATABASE_URL")
    default_nearest_limit: int = Field(default=20, alias="DEFAULT_NEAREST_LIMIT", ge=1)
    default_max_distance_m: Optional[float] = Field(
        default=None, alias="DEFAULT_MAX_DISTANCE_M", ge=0
    )

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", case_sensitive=False)

    @field_validator("default_max_distance_m", mode="before")
    @classmethod
    def _empty_to_none(cls, v: object) -> object:
        if isinstance(v, str) and v.strip() == "":
            return None
        return v


@lru_cache
def get_settings() -> Settings:
    """Return cached application settings."""

    return Settings()
