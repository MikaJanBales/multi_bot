import os

from dotenv import load_dotenv

load_dotenv()

API_UNSPLASH = str(os.getenv("API_UNSPLASH"))
API_WEATHER = str(os.getenv("API_WEATHER"))
API_TELEGRAM = str(os.getenv("API_TELEGRAM"))
API_CONVERT = str(os.getenv("API_CONVERT"))
