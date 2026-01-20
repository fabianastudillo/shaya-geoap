-- Enable PostGIS
CREATE EXTENSION IF NOT EXISTS postgis;

-- Access points table with geography for distance calculations in meters
CREATE TABLE IF NOT EXISTS access_points (
    id BIGSERIAL PRIMARY KEY,
    ap_code TEXT NOT NULL UNIQUE,
    campus TEXT NOT NULL,
    building TEXT NOT NULL,
    floor TEXT NOT NULL,
    status TEXT,
    reference TEXT,
    altitude_m DOUBLE PRECISION,
    location GEOGRAPHY(POINTZ, 4326) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_access_points_location ON access_points USING GIST (location);

-- Keep timestamps fresh on updates
CREATE OR REPLACE FUNCTION set_access_points_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_access_points_updated_at ON access_points;
CREATE TRIGGER trg_access_points_updated_at
BEFORE UPDATE ON access_points
FOR EACH ROW EXECUTE FUNCTION set_access_points_updated_at();
