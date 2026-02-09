from src.load.db import get_conn
from src.extract.weather_client import fetch_weather
from src.transform.normalize import normalize_daily
from src.load.loaders import insert_raw_response, upsert_daily_weather
from src.quality.checks import run_quality_checks

# API uses latitude and longitude values to pull weather data for that location
CITIES = [
    ("London", 51.5072, -0.1276),
    ("Manchester", 53.4808, -2.2426),
    ("Birmingham", 52.4862, -1.8904),
    ("Leeds", 53.8008, -1.5491),
    ("Glasgow", 55.8642, -4.2518),
]

def apply_schema(conn) -> None:
    with open("sql/schema.sql", "r", encoding="utf-8") as f:
        sql = f.read()
    with conn.cursor() as cur:
        cur.execute(sql)

def main() -> None:
    source = "open-meteo"

    with get_conn() as conn:
        apply_schema(conn)

        total_rows = 0
        for city, lat, lon in CITIES:
            result = fetch_weather(lat, lon)
            request_url = result["request_url"]
            payload = result["payload"]

            insert_raw_response(conn, source=source, city=city, request_url=request_url, payload=payload)

            rows = normalize_daily(payload, city)
            total_rows += upsert_daily_weather(conn, rows)

        run_quality_checks(conn)

    print(f"Pipeline completed. Upserted {total_rows} daily rows across {len(CITIES)} cities.")

if __name__ == "__main__":
    main()
