
#!python -m spacy download en_core_web_sm
#pip install dateparser

import re
from datetime import datetime, timedelta
from dateparser.search import search_dates
from geopy.geocoders import Nominatim
import requests
import spacy
import ipywidgets as widgets
from IPython.display import display, clear_output

# Load spaCy model (small English)
nlp = spacy.load("en_core_web_sm")

def extract_info(query):
    doc = nlp(query)
    cities = [ent.text for ent in doc.ents if ent.label_ == "GPE"]

    city = cities[0] if cities else None

    if not city:
        known_cities = ["Dakar", "Cairo", "Nairobi", "Paris", "London", "New York", "Lagos"]
        query_words = [w.strip(",.?").title() for w in query.split()]
        for word in query_words:
            if word in known_cities:
                city = word
                break

    if not city:
        return {"error": "City not found in query"}

    geolocator = Nominatim(user_agent="geoapi")
    location = geolocator.geocode(city, timeout=10)
    if not location:
        return {"error": "Could not resolve city to coordinates"}

    latitude = location.latitude
    longitude = location.longitude

    # Handle "next N days"
    match = re.search(r"next\s+(\d+)\s+day", query.lower())
    if match:
        days = int(match.group(1))
        start_date = datetime.today().date()
        end_date = start_date + timedelta(days=days - 1)
    else:
        dates = search_dates(query)
        if dates:
            parsed_dates = sorted(set([d[1].date() for d in dates]))
            if len(parsed_dates) == 1:
                start_date = end_date = parsed_dates[0]
            else:
                start_date, end_date = parsed_dates[0], parsed_dates[-1]
        else:
            start_date = end_date = datetime.today().date()

    return {
        "city": city,
        "latitude": latitude,
        "longitude": longitude,
        "start_date": start_date,
        "end_date": end_date
    }


def get_weather_info(query):
    info = extract_info(query)
    if "error" in info:
        return info["error"]

    city = info["city"]
    lat = info["latitude"]
    lon = info["longitude"]
    start_date_obj = info["start_date"]
    end_date_obj = info["end_date"]

    start_date = start_date_obj.isoformat()
    end_date = end_date_obj.isoformat()

    today = datetime.today().date()

    # Use archive API for past dates, forecast for today/future
    if end_date_obj < today:
        base_url = "https://archive-api.open-meteo.com/v1/archive?"
    else:
        base_url = "https://api.open-meteo.com/v1/forecast?"

    url = (
        f"{base_url}"
        f"latitude={lat}&longitude={lon}&start_date={start_date}&end_date={end_date}"
        f"&daily=temperature_2m_max,temperature_2m_min,precipitation_sum&timezone=auto"
    )

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
    except requests.RequestException as e:
        return f"Failed to get weather data: {e}"

    daily = data.get("daily", {})
    dates = daily.get("time", [])
    temps_max = daily.get("temperature_2m_max", [])
    temps_min = daily.get("temperature_2m_min", [])
    rain = daily.get("precipitation_sum", [])

    if not dates:
        return "No weather data found for the given dates"

    result = f"Weather in {city} from {start_date} to {end_date}:\n"
    for i in range(len(dates)):
        max_temp = temps_max[i] if temps_max[i] is not None else "N/A"
        min_temp = temps_min[i] if temps_min[i] is not None else "N/A"
        rain_mm = rain[i] if rain[i] is not None else "N/A"
        result += (
            f"  {dates[i]}: Max {max_temp}°C, Min {min_temp}°C, Rain {rain_mm}mm\n"
        )

    return result
