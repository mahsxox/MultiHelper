import aiohttp
import os
from locales.translator import translate

API_KEY = os.getenv("WEATHER_API_KEY")

CITY_MAP = {
    "moscow": "Moscow",
    "spb": "Saint Petersburg"
}

async def get_weather(city_key: str, lang: str = "ru") -> str:
    city_name = CITY_MAP.get(city_key, "Saint Petersburg")
    url = "http://api.weatherstack.com/current"
    params = {
        "access_key": API_KEY,
        "query": city_name,
        "lang": lang
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as resp:
            data = await resp.json()

    if "current" not in data or "location" not in data:
        return translate("weather_error", lang)

    current = data["current"]
    location = data["location"]

    temp = current.get("temperature")
    weather_descriptions = current.get("weather_descriptions", [""])[0]
    humidity = current.get("humidity")
    wind_speed = current.get("wind_speed")
    city = location.get("name")
    country = location.get("country")

    return (
        f"{translate('weather_in', lang)} {city}, {country}:\n"
        f"⛅️ {weather_descriptions}\n"
        f"🌡 {translate('temperature', lang)}: {temp}°C\n"
        f"💧 {translate('humidity', lang)}: {humidity}%\n"
        f"💨 {translate('wind', lang)}: {wind_speed} км/ч"
    )