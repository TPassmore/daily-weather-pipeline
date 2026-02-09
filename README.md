# Daily Weather Pipeline

A small Python ETL pipeline that pulls daily weather forecasts from the Open-Meteo API, stores raw API payloads, normalizes daily metrics, and loads them into PostgreSQL for analysis.

## What It Does

- Extracts daily weather data for 5 UK cities:
  - London
  - Manchester
  - Birmingham
  - Leeds
  - Glasgow
- Stores raw JSON API responses in `raw.weather_api_responses`.
- Normalizes and upserts daily weather rows into `staging.daily_weather`.
- Runs built-in data quality checks after each pipeline run.
- Provides reusable analytics views in `sql/views.sql`.

## Tech Stack

- Python 3.11+
- PostgreSQL 16 (via Docker Compose)
- Libraries:
  - `requests`
  - `psycopg`
  - `python-dotenv`

## Project Structure

```text
.
|-- docker-compose.yaml
|-- .env
|-- sql
|   |-- schema.sql
|   `-- views.sql
`-- src
    |-- pipeline.py
    |-- config.py
    |-- extract/weather_client.py
    |-- transform/normalize.py
    |-- load/db.py
    |-- load/loaders.py
    `-- quality/checks.py
```

## Database Setup

Start PostgreSQL:

```bash
docker compose up -d
```

Default DB settings are already in `.env`:

```env
DB_HOST=localhost
DB_PORT=5433
DB_NAME=weather_dw
DB_USER=weather
DB_PASSWORD=weather
```

The pipeline auto-applies `sql/schema.sql` on startup.

## Python Setup

Create and activate a virtual environment, then install dependencies:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install requests psycopg[binary] python-dotenv
```

## Run the Pipeline

From the project root:

```bash
python -m src.pipeline
```

Successful run output looks like:

```text
Pipeline completed. Upserted <N> daily rows across 5 cities.
```

## Quality Checks

`src/quality/checks.py` enforces:

- No duplicate `(city, date)` rows in `staging.daily_weather`
- No rows where `temp_max < temp_min`
- At least one row loaded

The pipeline raises an error if any check fails.

## Analytics Views

Create or refresh views:

```sql
\i sql/views.sql
```

Provided views:

- `mart.latest_city_weather`: latest available day for each city
- `mart.city_7d_rolling`: 7-day rolling averages for max temp and precipitation
- `mart.rainy_days_by_city`: rainy day counts by city

## Example Queries

Latest city snapshot:

```sql
SELECT * FROM mart.latest_city_weather;
```

7-day rolling metrics:

```sql
SELECT *
FROM mart.city_7d_rolling
ORDER BY city, date DESC;
```

Rainy day ranking:

```sql
SELECT * FROM mart.rainy_days_by_city;
```

## Notes

- Source API: Open-Meteo (`https://api.open-meteo.com/v1/forecast`)
- Timezone used in API requests: `Europe/London`
- Upsert key is `(city, date)`, so reruns update existing dates instead of duplicating rows.
