CREATE TABLE IF NOT EXISTS operations.delivery_points (

    id BIGSERIAL PRIMARY KEY,

    operator VARCHAR(50) NOT NULL,

    external_id VARCHAR(255),

    type VARCHAR(50),

    name TEXT,

    city TEXT,

    postal_code VARCHAR(20),

    street TEXT,

    opening_hours TEXT,

    cash_on_delivery BOOLEAN DEFAULT FALSE,

    latitude DOUBLE PRECISION,

    longitude DOUBLE PRECISION,

    geometry GEOMETRY(Point, 4326),

    created_at TIMESTAMP DEFAULT NOW()

);


CREATE INDEX IF NOT EXISTS idx_delivery_points_geometry
ON operations.delivery_points
USING GIST (geometry);


CREATE INDEX IF NOT EXISTS idx_delivery_points_operator
ON operations.delivery_points(operator);