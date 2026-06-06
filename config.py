import streamlit as st

try:
    GEMINI_API_KEY = st.secrets["AIzaSyB0pia4BoKmN9MxANH4USkupHLMeYq8iKY"]
except:
    GEMINI_API_KEY = "AIzaSyB0pia4BoKmN9MxANH4USkupHLMeYq8iKY"

try:
    WEATHER_API_KEY = st.secrets["6186e4f9d42ea1e07036b53bfd1848a4"]
except:
    WEATHER_API_KEY = "6186e4f9d42ea1e07036b53bfd1848a4"

APP_NAME = "AgroKhet AI"
APP_TAGLINE = "Smart Farming, Better Future"
APP_VERSION = "1.0.0"
DATABASE_NAME = "agrokhet.db"

LANGUAGES = {
    "English": "en",
    "Hindi": "hi",
    "Bengali": "bn",
    "Tamil": "ta",
    "Telugu": "te",
    "Marathi": "mr",
    "Gujarati": "gu",
    "Kannada": "kn",
    "Punjabi": "pa",
    "Odia": "or"
}

COLORS = {
    "primary_green": "#2E7D32",
    "light_green": "#81C784",
    "saffron": "#FF6F00",
    "golden": "#F9A825",
    "white": "#FFFFFF",
    "dark": "#1B1B1B",
    "bg_light": "#F1F8E9"
}

WEATHER_BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
FORECAST_BASE_URL = "https://api.openweathermap.org/data/2.5/forecast"
DEFAULT_CITY = "Delhi"