import io
from collections import Counter, defaultdict
from datetime import datetime

import matplotlib
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import requests

matplotlib.use("Agg")

GDANSK_LAT = 54.352
GDANSK_LON = 18.6466
OPEN_METEO_URL = "https://api.open-meteo.com/v1/forecast"
JSONPLACEHOLDER_BASE = "https://jsonplaceholder.typicode.com"


def fetch_weather():
    params = {
        "latitude": GDANSK_LAT,
        "longitude": GDANSK_LON,
        "hourly": "temperature_2m",
        "forecast_days": 1,
        "timezone": "Europe/Warsaw",
    }
    response = requests.get(OPEN_METEO_URL, params=params, timeout=10)
    response.raise_for_status()
    data = response.json()
    times = data["hourly"]["time"][:24]
    temps = data["hourly"]["temperature_2m"][:24]
    return times, temps


def get_current_temperature(temps):
    hour = datetime.now().hour
    return temps[hour] if hour < len(temps) else temps[0]


def generate_weather_chart(times, temps):
    dt_times = [datetime.strptime(t, "%Y-%m-%dT%H:%M") for t in times]

    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(dt_times, temps, color="#2196F3", linewidth=2, marker="o", markersize=4)
    ax.fill_between(dt_times, temps, alpha=0.15, color="#2196F3")
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))
    ax.xaxis.set_major_locator(mdates.HourLocator(interval=3))
    ax.set_xlabel("Godzina")
    ax.set_ylabel("Temperatura (°C)")
    ax.set_title("Prognoza temperatury dla Gdańska – 24h")
    ax.grid(True, alpha=0.3)
    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format="png", dpi=100)
    plt.close(fig)
    buf.seek(0)
    return buf.getvalue()


def get_weather_summary():
    times, temps = fetch_weather()
    return {
        "city": "Gdańsk",
        "date": times[0][:10] if times else None,
        "current_temperature": get_current_temperature(temps),
        "avg_temperature": round(sum(temps) / len(temps), 1),
        "min_temperature": min(temps),
        "max_temperature": max(temps),
        "unit": "°C",
    }


def fetch_users_with_post_counts():
    users_resp = requests.get(f"{JSONPLACEHOLDER_BASE}/users", timeout=10)
    users_resp.raise_for_status()

    posts_resp = requests.get(f"{JSONPLACEHOLDER_BASE}/posts", timeout=10)
    posts_resp.raise_for_status()

    users = users_resp.json()
    posts = posts_resp.json()

    post_counts = Counter(p["userId"] for p in posts)

    title_lengths = defaultdict(list)
    for p in posts:
        title_lengths[p["userId"]].append(len(p["title"]))

    result = []
    for user in users:
        uid = user["id"]
        count = post_counts.get(uid, 0)
        lengths = title_lengths.get(uid, [])
        avg_len = round(sum(lengths) / len(lengths), 1) if lengths else 0.0
        result.append({
            "id": uid,
            "name": user["name"],
            "username": user["username"],
            "email": user["email"],
            "post_count": count,
            "avg_title_length": avg_len,
        })

    result.sort(key=lambda x: x["post_count"], reverse=True)
    return result