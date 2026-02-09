CREATE SCHEMA IF NOT EXISTS raw;
CREATE SCHEMA IF NOT EXISTS staging;

CREATE TABLE IF NOT EXISTS raw.weather_api_responses (
  ingestion_id uuid PRIMARY KEY,
  source text NOT NULL,
  city text NOT NULL,
  request_url text NOT NULL,
  ingested_at timestamptz NOT NULL,
  payload jsonb NOT NULL
);

CREATE TABLE IF NOT EXISTS staging.daily_weather (
  city text NOT NULL,
  date date NOT NULL,
  temp_max numeric,
  temp_min numeric,
  precip_sum numeric,
  wind_max numeric,
  ingested_at timestamptz NOT NULL,
  PRIMARY KEY (city, date)
);
