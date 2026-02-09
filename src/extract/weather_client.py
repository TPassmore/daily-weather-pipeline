from typing import Dict, Any
import requests

BASE_URL = "https://api.open-meteo.com/v1/forecast"

def build_url(lat: float, lon: float) -> str:
    params = {
        "latitude": lat,
        "longitude": lon,
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum,windspeed_10m_max",
        "timezone": "Europe/London",
    }
    req = requests.Request("GET", BASE_URL, params=params).prepare()
    return req.url

def fetch_weather(lat: float, lon: float) -> Dict[str, Any]:
    url = build_url(lat, lon)
    r = requests.get(url, timeout=30)
    r.raise_for_status()
    return {"request_url": url, "payload": r.json()}
