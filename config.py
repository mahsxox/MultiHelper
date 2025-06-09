import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///reminders.db")

GOOGLE_SHEETS_JSON = os.getenv("GOOGLE_SHEETS_JSON")

DEFAULT_LANGUAGE = "ru"
