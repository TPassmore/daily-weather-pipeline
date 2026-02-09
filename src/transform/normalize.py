from datetime import datetime, timezone
from typing import Any, Dict, List


def normalize_daily(payload: Dict[str, Any], city: str) -> List[Dict[str, Any]]:
    daily = payload.get("daily", {})
    dates = daily.get("time", [])

    tmax = daily.get("temperature_2m_max", [])
    tmin = daily.get("temperature_2m_min", [])
    precip = daily.get("precipitation_sum", [])
    wind = daily.get("windspeed_10m_max", [])

    ingested_at = datetime.now(timezone.utc)

    rows = []
    for i, d in enumerate(dates):
        rows.append(
            {
                "city": city,
                "date": d,
                "temp_max": tmax[i] if i < len(tmax) else None,
                "temp_min": tmin[i] if i < len(tmin) else None,
                "precip_sum": precip[i] if i < len(precip) else None,
                "wind_max": wind[i] if i < len(wind) else None,
                "ingested_at": ingested_at,
            }
        )
    return rows
