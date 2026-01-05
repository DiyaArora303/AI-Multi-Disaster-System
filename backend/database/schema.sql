-- database/schema.sql
CREATE EXTENSION IF NOT EXISTS postgis;

CREATE TABLE IF NOT EXISTS zones (
  id SERIAL PRIMARY KEY,
  name TEXT,
  geom geometry(Polygon, 4326),
  admin_level TEXT
);

CREATE TABLE IF NOT EXISTS disasters (
  id SERIAL PRIMARY KEY,
  disaster_type TEXT NOT NULL,
  probability REAL,
  severity TEXT,
  timestamp TIMESTAMP DEFAULT now(),
  geometry geometry(Geometry, 4326),
  metadata JSONB
);

CREATE TABLE IF NOT EXISTS alerts (
  id SERIAL PRIMARY KEY,
  title TEXT,
  message TEXT,
  disaster_type TEXT,
  level TEXT,
  issued_at TIMESTAMP DEFAULT now(),
  geometry geometry(Geometry, 4326),
  sent boolean DEFAULT false,
  recipients JSONB,
  extra JSONB
);

CREATE TABLE IF NOT EXISTS population_risk (
  id SERIAL PRIMARY KEY,
  zone_id INT REFERENCES zones(id),
  population_at_risk BIGINT,
  calculated_at TIMESTAMP DEFAULT now()
);
