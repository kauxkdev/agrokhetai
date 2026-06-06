# =============================================
#         AgroKhet AI - Home Dashboard
# =============================================

import streamlit as st
import datetime
from config import COLORS

def show():

    user = st.session_state.user
    now = datetime.datetime.now()
    hour = now.hour

    # --- GREETING ---
    if hour < 12:
        greeting = "Good Morning"
        emoji = "🌅"
    elif hour < 17:
        greeting = "Good Afternoon"
        emoji = "☀️"
    else:
        greeting = "Good Evening"
        emoji = "🌙"

    # --- NAVBAR ---
    st.markdown(f"""
    <div class="navbar">
        <div class="navbar-brand">🌾 AgroKhet AI</div>
        <div class="navbar-user">
            👤 {user['full_name']} |
            📍 {user['state']} |
            🌐 {user['language']}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # --- WELCOME BANNER ---
    st.markdown(f"""
    <div style="
        background: linear-gradient(
            135deg,
            #1B5E20,
            #2E7D32,
            #FF6F00
        );
        border-radius: 24px;
        padding: 32px;
        color: white;
        margin-bottom: 28px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.15);
    ">
        <div style="font-size:48px;">{emoji}</div>
        <div style="
            font-family:'Rajdhani',sans-serif;
            font-size:32px;
            font-weight:700;
            margin-top:8px;
        ">
            {greeting}, {user['full_name']}!
        </div>
        <div style="
            font-size:16px;
            opacity:0.9;
            margin-top:8px;
        ">
            Welcome to AgroKhet AI —
            Your Smart Farming Assistant 🚀
        </div>
        <div style="
            font-size:14px;
            opacity:0.7;
            margin-top:6px;
        ">
            📅 {now.strftime("%A, %d %B %Y")} |
            ⏰ {now.strftime("%I:%M %p")}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # --- QUICK STATS ---
    st.markdown("""
    <div class="section-header">
        📊 Quick Overview
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown("""
        <div class="card">
            <div class="card-icon">🌿</div>
            <div class="card-title">Crop Scans</div>
            <div class="card-value">0</div>
            <div style="font-size:12px;color:#888;">
                Total scans done
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="card" style="border-color:#FF6F00;">
            <div class="card-icon">🚜</div>
            <div class="card-title">My Crops</div>
            <div class="card-value">0</div>
            <div style="font-size:12px;color:#888;">
                Active crops
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="card" style="border-color:#1565C0;">
            <div class="card-icon">💧</div>
            <div class="card-title">Water Alerts</div>
            <div class="card-value">0</div>
            <div style="font-size:12px;color:#888;">
                Pending alerts
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown("""
        <div class="card" style="border-color:#F9A825;">
            <div class="card-icon">💰</div>
            <div class="card-title">Market Tips</div>
            <div class="card-value">3</div>
            <div style="font-size:12px;color:#888;">
                Today's tips
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # --- QUICK ACCESS BUTTONS ---
    st.markdown("""
    <div class="section-header">
        ⚡ Quick Access
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button(
            "🌿 Scan Crop Disease",
            use_container_width=True
        ):
            st.session_state.page = "crop_scanner"
            st.rerun()

        if st.button(
            "💰 Check Market Price",
            use_container_width=True
        ):
            st.session_state.page = "market"
            st.rerun()

        if st.button(
            "📰 Agriculture News",
            use_container_width=True
        ):
            st.session_state.page = "news"
            st.rerun()

    with col2:
        if st.button(
            "🌦️ Check Weather",
            use_container_width=True
        ):
            st.session_state.page = "weather"
            st.rerun()

        if st.button(
            "📅 Crop Calendar",
            use_container_width=True
        ):
            st.session_state.page = "crop_calendar"
            st.rerun()

        if st.button(
            "🌳 Plant Information",
            use_container_width=True
        ):
            st.session_state.page = "plant_info"
            st.rerun()

    with col3:
        if st.button(
            "🤖 Ask AgroBot",
            use_container_width=True
        ):
            st.session_state.page = "agrobot"
            st.rerun()

        if st.button(
            "💧 Water & Land",
            use_container_width=True
        ):
            st.session_state.page = "water_land"
            st.rerun()

        if st.button(
            "🚜 My Farm",
            use_container_width=True
        ):
            st.session_state.page = "my_farm"
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # --- DAILY TIPS ---
    st.markdown("""
    <div class="section-header">
        💡 Today's Farming Tips
    </div>
    """, unsafe_allow_html=True)

    tips = [
        {
            "icon": "🌱",
            "title": "Soil Health",
            "tip": "Test your soil pH before sowing. "
                   "Most crops grow best in pH 6.0-7.0."
        },
        {
            "icon": "💧",
            "title": "Water Management",
            "tip": "Water crops early morning to reduce "
                   "evaporation and prevent fungal disease."
        },
        {
            "icon": "🌾",
            "title": "Crop Rotation",
            "tip": "Rotate crops every season to maintain "
                   "soil nutrients and reduce pests."
        },
    ]

    col1, col2, col3 = st.columns(3)
    cols = [col1, col2, col3]

    for i, tip in enumerate(tips):
        with cols[i]:
            st.markdown(f"""
            <div class="card">
                <div class="card-icon">{tip['icon']}</div>
                <div class="card-title">{tip['title']}</div>
                <div style="
                    font-size:14px;
                    color:#555;
                    margin-top:8px;
                    line-height:1.6;
                ">
                    {tip['tip']}
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # --- SEASON INFO ---
    month = now.month
    if month in [6, 7, 8, 9]:
        season = "🌧️ Kharif Season"
        season_crops = "Rice, Maize, Cotton, Soybean, Groundnut"
        season_color = "#1565C0"
    elif month in [10, 11, 12, 1, 2, 3]:
        season = "❄️ Rabi Season"
        season_crops = "Wheat, Mustard, Peas, Gram, Barley"
        season_color = "#6A1B9A"
    else:
        season = "☀️ Zaid Season"
        season_crops = "Watermelon, Cucumber, Muskmelon, Moong"
        season_color = "#E65100"

    st.markdown(f"""
    <div style="
        background: linear-gradient(
            135deg,
            {season_color},
            {season_color}99
        );
        border-radius: 20px;
        padding: 24px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
    ">
        <div style="
            font-family:'Rajdhani',sans-serif;
            font-size:26px;
            font-weight:700;
        ">
            Current Season: {season}
        </div>
        <div style="
            font-size:16px;
            opacity:0.9;
            margin-top:8px;
        ">
            🌾 Best Crops Now: {season_crops}
        </div>
        <div style="
            font-size:13px;
            opacity:0.7;
            margin-top:6px;
        ">
            Click Crop Calendar for detailed schedule
        </div>
    </div>
    """, unsafe_allow_html=True)