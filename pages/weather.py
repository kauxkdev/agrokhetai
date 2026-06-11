# =============================================
#         AgroKhet AI - Weather Page
# =============================================

import streamlit as st
import requests
from config import WEATHER_API_KEY, DEFAULT_CITY
import datetime

# --- GET CURRENT WEATHER ---
def get_weather(city):
    try:
        url = (
            f"https://api.openweathermap.org"
            f"/data/2.5/weather"
            f"?q={city}"
            f"&appid={WEATHER_API_KEY}"
            f"&units=metric"
        )
        response = requests.get(url)
        return response.json()
    except:
        return None

# --- GET 5 DAY FORECAST ---
def get_forecast(city):
    try:
        url = (
            f"https://api.openweathermap.org"
            f"/data/2.5/forecast"
            f"?q={city}"
            f"&appid={WEATHER_API_KEY}"
            f"&units=metric"
        )
        response = requests.get(url)
        return response.json()
    except:
        return None

# --- WEATHER EMOJI ---
def get_weather_emoji(condition):
    condition = condition.lower()
    if "rain" in condition:
        return "🌧️"
    elif "cloud" in condition:
        return "☁️"
    elif "clear" in condition:
        return "☀️"
    elif "storm" in condition:
        return "⛈️"
    elif "snow" in condition:
        return "❄️"
    elif "mist" in condition or "fog" in condition:
        return "🌫️"
    elif "wind" in condition:
        return "💨"
    else:
        return "🌤️"

# --- FARMING ADVICE BASED ON WEATHER ---
def get_farming_advice(temp, humidity, condition):
    advice = []
    condition = condition.lower()

    if "rain" in condition:
        advice.append(
            "🌧️ Rain expected — avoid pesticide spraying today"
        )
        advice.append(
            "💧 Check field drainage to avoid waterlogging"
        )
        advice.append(
            "🌱 Good time for transplanting seedlings"
        )
    elif "clear" in condition:
        advice.append(
            "☀️ Clear sky — good day for harvesting"
        )
        advice.append(
            "🌾 Ideal conditions for pesticide spraying"
        )
        advice.append(
            "💧 Water your crops in early morning"
        )

    if temp > 35:
        advice.append(
            "🌡️ Very hot — increase irrigation frequency"
        )
        advice.append(
            "🌿 Protect crops from heat stress"
        )
    elif temp < 10:
        advice.append(
            "❄️ Cold weather — protect crops from frost"
        )
        advice.append(
            "🌱 Delay sowing sensitive crops"
        )

    if humidity > 80:
        advice.append(
            "💦 High humidity — watch for fungal diseases"
        )
    elif humidity < 30:
        advice.append(
            "🏜️ Low humidity — increase watering schedule"
        )

    return advice if advice else [
        "✅ Weather is suitable for normal farming activities"
    ]

# --- MAIN SHOW FUNCTION ---
def show():

    user = st.session_state.user

    # --- NAVBAR ---
    st.markdown(f"""
    <div class="navbar">
        <div class="navbar-brand">🌾 AgroKhet AI</div>
        <div class="navbar-user">
            🌦️ Weather | 👤 {user['full_name']}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # --- HEADER ---
    st.markdown("""
    <div class="section-header">
        🌦️ Weather & Farming Advisory
    </div>
    """, unsafe_allow_html=True)

    # --- CITY INPUT ---
    col1, col2 = st.columns([3, 1])
    with col1:
        city = st.text_input(
            "🏙️ Enter Your City",
            value=user.get('state', DEFAULT_CITY),
            placeholder="Enter city name..."
        )
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        search = st.button(
            "🔍 Get Weather",
            use_container_width=True
        )

    if city:
        # --- FETCH WEATHER ---
        with st.spinner("Fetching weather data..."):
            weather_data = get_weather(city)
            forecast_data = get_forecast(city)

        if weather_data and weather_data.get('cod') == 200:

            # Extract data
            temp = weather_data['main']['temp']
            feels_like = weather_data['main']['feels_like']
            humidity = weather_data['main']['humidity']
            wind = weather_data['wind']['speed']
            condition = weather_data['weather'][0]['main']
            description = (
                weather_data['weather'][0]['description']
            )
            visibility = weather_data.get(
                'visibility', 0
            ) / 1000
            pressure = weather_data['main']['pressure']

            weather_emoji = get_weather_emoji(condition)

            # --- MAIN WEATHER CARD ---
            st.markdown(f"""
            <div class="weather-card">
                <div style="font-size:80px;">
                    {weather_emoji}
                </div>
                <div class="weather-temp">
                    {temp:.1f}°C
                </div>
                <div class="weather-city">
                    📍 {city.title()}
                </div>
                <div class="weather-desc">
                    {description}
                </div>
                <div style="
                    margin-top:20px;
                    font-size:14px;
                    opacity:0.8;
                ">
                    🌡️ Feels like {feels_like:.1f}°C
                </div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            # --- WEATHER DETAILS ---
            st.markdown("""
            <div class="section-header">
                📊 Weather Details
            </div>
            """, unsafe_allow_html=True)

            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.markdown(f"""
                <div class="card">
                    <div class="card-icon">💧</div>
                    <div class="card-title">Humidity</div>
                    <div class="card-value">
                        {humidity}%
                    </div>
                </div>
                """, unsafe_allow_html=True)

            with col2:
                st.markdown(f"""
                <div class="card"
                     style="border-color:#1565C0;">
                    <div class="card-icon">💨</div>
                    <div class="card-title">Wind Speed</div>
                    <div class="card-value">
                        {wind} m/s
                    </div>
                </div>
                """, unsafe_allow_html=True)

            with col3:
                st.markdown(f"""
                <div class="card"
                     style="border-color:#FF6F00;">
                    <div class="card-icon">👁️</div>
                    <div class="card-title">Visibility</div>
                    <div class="card-value">
                        {visibility:.1f} km
                    </div>
                </div>
                """, unsafe_allow_html=True)

            with col4:
                st.markdown(f"""
                <div class="card"
                     style="border-color:#6A1B9A;">
                    <div class="card-icon">🌡️</div>
                    <div class="card-title">Pressure</div>
                    <div class="card-value">
                        {pressure}
                    </div>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            # --- FARMING ADVICE ---
            st.markdown("""
            <div class="section-header">
                🌾 Today's Farming Advisory
            </div>
            """, unsafe_allow_html=True)

            advice_list = get_farming_advice(
                temp, humidity, condition
            )

            for advice in advice_list:
                st.markdown(f"""
                <div style="
                    background: #E8F5E9;
                    border-radius: 12px;
                    padding: 14px 20px;
                    margin-bottom: 10px;
                    border-left: 4px solid #2E7D32;
                    font-size: 15px;
                    color: #1B5E20;
                    font-weight: 500;
                ">
                    {advice}
                </div>
                """, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            # --- 5 DAY FORECAST ---
            if forecast_data and \
                forecast_data.get('cod') == '200':

                st.markdown("""
                <div class="section-header">
                    📅 5 Day Forecast
                </div>
                """, unsafe_allow_html=True)

                # Get one forecast per day
                seen_dates = []
                forecast_list = []

                for item in forecast_data['list']:
                    date = item['dt_txt'].split(' ')[0]
                    if date not in seen_dates:
                        seen_dates.append(date)
                        forecast_list.append(item)
                    if len(forecast_list) == 5:
                        break

                cols = st.columns(5)

                for i, item in enumerate(forecast_list):
                    with cols[i]:
                        f_temp = item['main']['temp']
                        f_cond = (
                            item['weather'][0]['main']
                        )
                        f_emoji = get_weather_emoji(
                            f_cond
                        )
                        f_date = datetime.datetime.strptime(
                            item['dt_txt'],
                            "%Y-%m-%d %H:%M:%S"
                        )
                        f_day = f_date.strftime("%a")
                        f_day_num = f_date.strftime("%d %b")

                        st.markdown(f"""
                        <div class="card" style="
                            text-align:center;
                            padding:16px;
                        ">
                            <div style="
                                font-weight:600;
                                color:#1B5E20;
                                font-size:14px;
                            ">
                                {f_day}
                            </div>
                            <div style="
                                font-size:11px;
                                color:#888;
                            ">
                                {f_day_num}
                            </div>
                            <div style="font-size:32px;">
                                {f_emoji}
                            </div>
                            <div style="
                                font-size:20px;
                                font-weight:700;
                                color:#FF6F00;
                            ">
                                {f_temp:.0f}°C
                            </div>
                            <div style="
                                font-size:11px;
                                color:#888;
                            ">
                                {f_cond}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

        else:
            st.error(
                "❌ City not found! "
                "Please check the city name."
            )
            st.info(
                "💡 Try entering city name in English "
                "like: Delhi, Mumbai, Lucknow"
            )