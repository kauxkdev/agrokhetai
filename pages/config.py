# =============================================
#         AgroKhet AI - Configuration File
# =============================================

import streamlit as st
# --- API KEYS ---
try:
    GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
    WEATHER_API_KEY = st.secrets["WEATHER_API_KEY"]
except:
    GEMINI_API_KEY = "AQ.Ab8RN6ImU7Mev6YsQ1mRFubzyrfgSozyKY5_i1U1CXdk8tVUfQ"
    WEATHER_API_KEY = "6186e4f9d42ea1e07036b53bfd1848a4"

# --- APP SETTINGS ---
APP_NAME = "AgroKhet AI"
APP_TAGLINE = "Smart Farming, Better Future"
APP_VERSION = "1.0.0"

# --- DATABASE ---
DATABASE_NAME = "agrokhet.db"

# --- SUPPORTED LANGUAGES ---
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

# --- APP COLORS ---
COLORS = {
    "primary_green": "#2E7D32",
    "light_green": "#81C784",
    "saffron": "#FF6F00",
    "golden": "#F9A825",
    "white": "#FFFFFF",
    "dark": "#1B1B1B",
    "bg_light": "#F1F8E9"
}

# --- WEATHER SETTINGS ---
WEATHER_BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
FORECAST_BASE_URL = "https://api.openweathermap.org/data/2.5/forecast"

# --- DEFAULT CITY ---
DEFAULT_CITY = "Delhi"
