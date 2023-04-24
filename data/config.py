import os

from dotenv import load_dotenv

load_dotenv()

API_UNSPLASH = str(os.getenv("API_UNSPLASH"))  # токен Exchange Rate API
API_WEATHER = str(os.getenv("API_WEATHER"))  # токен OpenWeatherMap API
API_TELEGRAM = str(os.getenv("API_TELEGRAM"))  # токен телеграма от @bot_father
API_CONVERT = str(os.getenv("API_CONVERT"))  # токен Exchange Rate API

admins_id = []
