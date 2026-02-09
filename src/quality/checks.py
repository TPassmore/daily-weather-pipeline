def run_quality_checks(conn) -> None:
    with conn.cursor() as cur:
        cur.execute("""
            SELECT city, date, COUNT(*)
            FROM staging.daily_weather
            GROUP BY city, date
            HAVING COUNT(*) > 1
        """)
        dupes = cur.fetchall()
        if dupes:
            raise RuntimeError(f"Duplicate (city,date) rows found: {dupes[:5]}")

        cur.execute("""
            SELECT COUNT(*)
            FROM staging.daily_weather
            WHERE temp_max IS NOT NULL AND temp_min IS NOT NULL AND temp_max < temp_min
        """)
        bad = cur.fetchone()[0]
        if bad > 0:
            raise RuntimeError(f"Found {bad} rows where temp_max < temp_min")

        cur.execute("SELECT COUNT(*) FROM staging.daily_weather")
        total = cur.fetchone()[0]
        if total < 1:
            raise RuntimeError("No rows in staging.daily_weather after load")
