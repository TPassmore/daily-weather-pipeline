import uuid

from datetime import datetime, timezone
from typing import Any, Dict, List
from psycopg.types.json import Json

def insert_raw_response(conn, *, source: str, city: str, request_url: str, payload: Dict[str, Any]) -> uuid.UUID:
    ingestion_id = uuid.uuid4()
    ingested_at = datetime.now(timezone.utc)

    with conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO raw.weather_api_responses
            (ingestion_id, source, city, request_url, ingested_at, payload)
            VALUES (%s, %s, %s, %s, %s, %s::jsonb)
            """,
            (ingestion_id, source, city, request_url, ingested_at, Json(payload)),
        )
    return ingestion_id

def upsert_daily_weather(conn, rows: List[Dict[str, Any]]) -> int:
    if not rows:
        return 0

    with conn.cursor() as cur:
        cur.executemany(
            """
            INSERT INTO staging.daily_weather
              (city, date, temp_max, temp_min, precip_sum, wind_max, ingested_at)
            VALUES
              (%(city)s, %(date)s, %(temp_max)s, %(temp_min)s, %(precip_sum)s, %(wind_max)s, %(ingested_at)s)
            ON CONFLICT (city, date)
            DO UPDATE SET
              temp_max = EXCLUDED.temp_max,
              temp_min = EXCLUDED.temp_min,
              precip_sum = EXCLUDED.precip_sum,
              wind_max = EXCLUDED.wind_max,
              ingested_at = EXCLUDED.ingested_at
            """,
            rows,
        )
    return len(rows)
