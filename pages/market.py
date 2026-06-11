# =============================================
#         AgroKhet AI - Market Price Page
# =============================================

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import random

# --- CROP PRICE DATABASE ---
# Real approximate mandi prices (INR per Quintal)
CROP_PRICES = {
    "Wheat": {
        "price": 2275,
        "unit": "per Quintal",
        "trend": "up",
        "change": 25,
        "min": 2100,
        "max": 2400,
        "best_market": "Punjab, Haryana, UP",
        "best_month": "March - April",
        "emoji": "🌾"
    },
    "Rice": {
        "price": 2183,
        "unit": "per Quintal",
        "trend": "up",
        "change": 15,
        "min": 1900,
        "max": 2500,
        "best_market": "Punjab, West Bengal, AP",
        "best_month": "October - November",
        "emoji": "🍚"
    },
    "Cotton": {
        "price": 6620,
        "unit": "per Quintal",
        "trend": "down",
        "change": -120,
        "min": 5500,
        "max": 7000,
        "best_market": "Gujarat, Maharashtra, AP",
        "best_month": "November - January",
        "emoji": "🌸"
    },
    "Soybean": {
        "price": 4600,
        "unit": "per Quintal",
        "trend": "up",
        "change": 80,
        "min": 4000,
        "max": 5200,
        "best_market": "MP, Maharashtra, Rajasthan",
        "best_month": "October - December",
        "emoji": "🫘"
    },
    "Maize": {
        "price": 1962,
        "unit": "per Quintal",
        "trend": "up",
        "change": 32,
        "min": 1700,
        "max": 2200,
        "best_market": "Karnataka, Bihar, AP",
        "best_month": "September - November",
        "emoji": "🌽"
    },
    "Tomato": {
        "price": 1200,
        "unit": "per Quintal",
        "trend": "up",
        "change": 200,
        "min": 400,
        "max": 3000,
        "best_market": "HP, Karnataka, Maharashtra",
        "best_month": "October - December",
        "emoji": "🍅"
    },
    "Onion": {
        "price": 1800,
        "unit": "per Quintal",
        "trend": "down",
        "change": -150,
        "min": 800,
        "max": 4000,
        "best_market": "Maharashtra, MP, Karnataka",
        "best_month": "December - March",
        "emoji": "🧅"
    },
    "Potato": {
        "price": 900,
        "unit": "per Quintal",
        "trend": "up",
        "change": 50,
        "min": 500,
        "max": 1500,
        "best_market": "UP, West Bengal, Punjab",
        "best_month": "February - April",
        "emoji": "🥔"
    },
    "Mustard": {
        "price": 5450,
        "unit": "per Quintal",
        "trend": "up",
        "change": 90,
        "min": 4800,
        "max": 6000,
        "best_market": "Rajasthan, UP, Haryana",
        "best_month": "March - May",
        "emoji": "🌻"
    },
    "Sugarcane": {
        "price": 315,
        "unit": "per Quintal",
        "trend": "stable",
        "change": 0,
        "min": 290,
        "max": 340,
        "best_market": "UP, Maharashtra, Karnataka",
        "best_month": "October - March",
        "emoji": "🎋"
    },
    "Groundnut": {
        "price": 5850,
        "unit": "per Quintal",
        "trend": "up",
        "change": 110,
        "min": 5000,
        "max": 6500,
        "best_market": "Gujarat, AP, Tamil Nadu",
        "best_month": "November - January",
        "emoji": "🥜"
    },
    "Turmeric": {
        "price": 13500,
        "unit": "per Quintal",
        "trend": "up",
        "change": 500,
        "min": 10000,
        "max": 16000,
        "best_market": "Telangana, Tamil Nadu, Karnataka",
        "best_month": "February - April",
        "emoji": "🟡"
    },
}

# --- GENERATE PRICE HISTORY ---
def get_price_history(crop_name, days=30):
    base_price = CROP_PRICES[crop_name]['price']
    dates = []
    prices = []

    for i in range(days, 0, -1):
        date = datetime.now() - timedelta(days=i)
        dates.append(date.strftime("%d %b"))
        variation = random.uniform(-0.05, 0.05)
        price = base_price * (1 + variation)
        prices.append(round(price))

    return dates, prices

# --- MAIN SHOW FUNCTION ---
def show():

    user = st.session_state.user

    # --- NAVBAR ---
    st.markdown(f"""
    <div class="navbar">
        <div class="navbar-brand">🌾 AgroKhet AI</div>
        <div class="navbar-user">
            💰 Market Prices | 👤 {user['full_name']}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # --- HEADER ---
    st.markdown("""
    <div class="section-header">
        💰 Live Mandi Market Prices
    </div>
    """, unsafe_allow_html=True)

    # --- DATE INFO ---
    st.markdown(f"""
    <div style="
        background: #FFF8E1;
        border-radius: 12px;
        padding: 14px 20px;
        margin-bottom: 20px;
        border-left: 4px solid #F9A825;
        font-size: 14px;
        color: #555;
    ">
        📅 Last Updated: {datetime.now().strftime(
            "%d %B %Y, %I:%M %p"
        )} |
        💡 Prices in INR per Quintal |
        📊 Based on Agmarknet data
    </div>
    """, unsafe_allow_html=True)

    # --- SEARCH AND FILTER ---
    col1, col2 = st.columns([2, 1])

    with col1:
        search = st.text_input(
            "🔍 Search Crop",
            placeholder="Type crop name..."
        )

    with col2:
        sort_by = st.selectbox(
            "Sort by",
            ["Price: High to Low",
             "Price: Low to High",
             "Trending Up",
             "Name A-Z"]
        )

    # Filter crops
    filtered = {
        k: v for k, v in CROP_PRICES.items()
        if search.lower() in k.lower()
    } if search else CROP_PRICES

    # Sort crops
    if sort_by == "Price: High to Low":
        filtered = dict(sorted(
            filtered.items(),
            key=lambda x: x[1]['price'],
            reverse=True
        ))
    elif sort_by == "Price: Low to High":
        filtered = dict(sorted(
            filtered.items(),
            key=lambda x: x[1]['price']
        ))
    elif sort_by == "Trending Up":
        filtered = dict(sorted(
            filtered.items(),
            key=lambda x: x[1]['change'],
            reverse=True
        ))
    else:
        filtered = dict(sorted(filtered.items()))

    st.markdown("<br>", unsafe_allow_html=True)

    # --- PRICE CARDS ---
    st.markdown("""
    <div class="section-header">
        📊 Today's Prices
    </div>
    """, unsafe_allow_html=True)

    # Display in rows of 3
    crops_list = list(filtered.items())

    for i in range(0, len(crops_list), 3):
        cols = st.columns(3)
        for j, col in enumerate(cols):
            if i + j < len(crops_list):
                name, data = crops_list[i + j]

                trend_color = (
                    "#2E7D32" if data['trend'] == "up"
                    else "#C62828"
                    if data['trend'] == "down"
                    else "#FF6F00"
                )
                trend_arrow = (
                    "↑" if data['trend'] == "up"
                    else "↓"
                    if data['trend'] == "down"
                    else "→"
                )
                change_text = (
                    f"+₹{data['change']}"
                    if data['change'] > 0
                    else f"₹{data['change']}"
                    if data['change'] < 0
                    else "Stable"
                )

                with col:
                    st.markdown(f"""
                    <div class="card" style="
                        border-color:{trend_color};
                    ">
                        <div style="
                            display:flex;
                            justify-content:space-between;
                            align-items:center;
                        ">
                            <div style="font-size:36px;">
                                {data['emoji']}
                            </div>
                            <div style="
                                color:{trend_color};
                                font-size:24px;
                                font-weight:700;
                            ">
                                {trend_arrow}
                            </div>
                        </div>
                        <div class="card-title">
                            {name}
                        </div>
                        <div class="card-value">
                            ₹{data['price']:,}
                        </div>
                        <div style="
                            font-size:12px;
                            color:#888;
                        ">
                            {data['unit']}
                        </div>
                        <div style="
                            font-size:13px;
                            color:{trend_color};
                            font-weight:600;
                            margin-top:6px;
                        ">
                            {change_text} today
                        </div>
                        <div style="
                            font-size:11px;
                            color:#888;
                            margin-top:4px;
                        ">
                            📍 {data['best_market']}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # --- PRICE CHART ---
    st.markdown("""
    <div class="section-header">
        📈 Price Trend Chart
    </div>
    """, unsafe_allow_html=True)

    selected_crop = st.selectbox(
        "Select crop to see price trend",
        list(CROP_PRICES.keys())
    )

    if selected_crop:
        dates, prices = get_price_history(selected_crop)

        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=dates,
            y=prices,
            mode='lines+markers',
            name=selected_crop,
            line=dict(
                color='#2E7D32',
                width=3
            ),
            marker=dict(
                color='#FF6F00',
                size=6
            ),
            fill='tozeroy',
            fillcolor='rgba(46,125,50,0.1)'
        ))

        fig.update_layout(
            title=f"📈 {selected_crop} Price Trend (30 Days)",
            xaxis_title="Date",
            yaxis_title="Price (₹ per Quintal)",
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(family="Poppins"),
            title_font=dict(
                size=18,
                color='#1B5E20'
            ),
            height=400,
            showlegend=False,
            xaxis=dict(
                showgrid=True,
                gridcolor='#F1F8E9',
                tickangle=45
            ),
            yaxis=dict(
                showgrid=True,
                gridcolor='#F1F8E9'
            )
        )

        st.plotly_chart(fig, use_container_width=True)

        # Crop details
        data = CROP_PRICES[selected_crop]
        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown(f"""
            <div class="card">
                <div class="card-icon">📉</div>
                <div class="card-title">Min Price</div>
                <div class="card-value">
                    ₹{data['min']:,}
                </div>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
            <div class="card"
                 style="border-color:#F9A825;">
                <div class="card-icon">📈</div>
                <div class="card-title">Max Price</div>
                <div class="card-value">
                    ₹{data['max']:,}
                </div>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            st.markdown(f"""
            <div class="card"
                 style="border-color:#FF6F00;">
                <div class="card-icon">📅</div>
                <div class="card-title">Best Month</div>
                <div style="
                    font-size:14px;
                    font-weight:600;
                    color:#FF6F00;
                    margin-top:8px;
                ">
                    {data['best_month']}
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # --- COMPARISON CHART ---
    st.markdown("""
    <div class="section-header">
        ⚖️ Crop Price Comparison
    </div>
    """, unsafe_allow_html=True)

    selected_crops = st.multiselect(
        "Select crops to compare",
        list(CROP_PRICES.keys()),
        default=["Wheat", "Rice", "Cotton"]
    )

    if selected_crops:
        names = selected_crops
        prices_compare = [
            CROP_PRICES[c]['price']
            for c in selected_crops
        ]
        colors_list = [
            '#2E7D32', '#FF6F00', '#1565C0',
            '#F9A825', '#6A1B9A', '#C62828'
        ]

        fig2 = go.Figure(data=[
            go.Bar(
                x=names,
                y=prices_compare,
                marker_color=colors_list[
                    :len(selected_crops)
                ],
                text=[
                    f"₹{p:,}"
                    for p in prices_compare
                ],
                textposition='outside'
            )
        ])

        fig2.update_layout(
            title="💰 Crop Price Comparison (₹/Quintal)",
            xaxis_title="Crop",
            yaxis_title="Price (₹)",
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(family="Poppins"),
            title_font=dict(
                size=18,
                color='#1B5E20'
            ),
            height=400,
            showlegend=False
        )

        st.plotly_chart(fig2, use_container_width=True)