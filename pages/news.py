# =============================================
#         AgroKhet AI - News Page
# =============================================

import streamlit as st
from config import GEMINI_API_KEY
import datetime
from google import genai

# --- CONFIGURE GEMINI ---

# --- GET AI AGRICULTURE NEWS ---
def get_agri_news(category):
    try:
        client = genai.Client(api_key=GEMINI_API_KEY)
        prompt = f"""
        Give me 6 latest important agriculture
        news items for Indian farmers about:
        {category}

        For each news item provide:
        TITLE: (short catchy title)
        SUMMARY: (2-3 sentences summary)
        IMPORTANCE: (High/Medium/Low)
        ACTION: (What farmer should do)
        DATE: (approximate recent date)

        Make it practical and relevant for
        Indian farmers in 2025-2026.
        Separate each news with ---
        """
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents= prompt
        )
        return response.text
    except Exception as e:
        return f"❌ Error: {str(e)}"

# --- PARSE NEWS ---
def parse_news(raw_text):
    news_items = []
    items = raw_text.split("---")
    for item in items:
        if "TITLE:" in item:
            try:
                lines = item.strip().split("\n")
                news = {}
                for line in lines:
                    if line.startswith("TITLE:"):
                        news['title'] = line.replace(
                            "TITLE:", ""
                        ).strip()
                    elif line.startswith("SUMMARY:"):
                        news['summary'] = line.replace(
                            "SUMMARY:", ""
                        ).strip()
                    elif line.startswith(
                        "IMPORTANCE:"
                    ):
                        news['importance'] = (
                            line.replace(
                                "IMPORTANCE:", ""
                            ).strip()
                        )
                    elif line.startswith("ACTION:"):
                        news['action'] = line.replace(
                            "ACTION:", ""
                        ).strip()
                    elif line.startswith("DATE:"):
                        news['date'] = line.replace(
                            "DATE:", ""
                        ).strip()
                if news.get('title'):
                    news_items.append(news)
            except:
                pass
    return news_items

# --- GOVERNMENT SCHEMES ---
GOVT_SCHEMES = [
    {
        "name": "PM Kisan Samman Nidhi",
        "emoji": "💰",
        "benefit": "₹6000/year direct to bank",
        "eligibility": "All small/marginal farmers",
        "how_to": "Register at pmkisan.gov.in",
        "color": "#2E7D32"
    },
    {
        "name": "PM Fasal Bima Yojana",
        "emoji": "🛡️",
        "benefit": "Crop insurance at low premium",
        "eligibility": "All farmers growing notified crops",
        "how_to": "Apply through bank or CSC center",
        "color": "#1565C0"
    },
    {
        "name": "Kisan Credit Card",
        "emoji": "💳",
        "benefit": "Low interest crop loans",
        "eligibility": "All farmers",
        "how_to": "Apply at nearest bank branch",
        "color": "#FF6F00"
    },
    {
        "name": "PM Krishi Sinchai Yojana",
        "emoji": "💧",
        "benefit": "Subsidy on irrigation equipment",
        "eligibility": "Farmers with land ownership",
        "how_to": "Apply at agriculture department",
        "color": "#6A1B9A"
    },
    {
        "name": "Soil Health Card Scheme",
        "emoji": "🌍",
        "benefit": "Free soil testing and advice",
        "eligibility": "All farmers",
        "how_to": "Visit nearest Krishi Vigyan Kendra",
        "color": "#795548"
    },
    {
        "name": "eNAM Portal",
        "emoji": "📱",
        "benefit": "Sell crops online at best price",
        "eligibility": "All farmers",
        "how_to": "Register at enam.gov.in",
        "color": "#F9A825"
    },
]

# --- MAIN SHOW FUNCTION ---
def show():

    user = st.session_state.user

    # --- NAVBAR ---
    st.markdown(f"""
    <div class="navbar">
        <div class="navbar-brand">🌾 AgroKhet AI</div>
        <div class="navbar-user">
            📰 News | 👤 {user['full_name']}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # --- HEADER ---
    st.markdown("""
    <div class="section-header">
        📰 Agriculture News & Updates
    </div>
    """, unsafe_allow_html=True)

    # --- DATE ---
    st.markdown(f"""
    <div style="
        background: #FFF8E1;
        border-radius: 12px;
        padding: 12px 20px;
        margin-bottom: 20px;
        border-left: 4px solid #F9A825;
        font-size: 14px;
        color: #555;
    ">
        📅 Today: {datetime.datetime.now().strftime(
            "%A, %d %B %Y"
        )} |
        🌾 Latest agriculture updates for
        Indian farmers
    </div>
    """, unsafe_allow_html=True)

    # --- TABS ---
    tab1, tab2, tab3 = st.tabs([
        "📰 Latest News",
        "📋 Govt Schemes",
        "🌾 Seasonal Advisory"
    ])

    # ==========================
    #    TAB 1 - LATEST NEWS
    # ==========================
    with tab1:
        st.markdown("<br>", unsafe_allow_html=True)

        # News categories
        categories = [
            "🌾 Crop Prices & Market",
            "🌧️ Weather & Monsoon",
            "🐛 Pest & Disease Alert",
            "💰 Government Schemes",
            "🌱 New Farming Technology",
            "📦 Export & Import Policy"
        ]

        selected_cat = st.selectbox(
            "📂 Select News Category",
            categories
        )

        if st.button(
            "🔄 Load Latest News",
            use_container_width=True
        ):
            with st.spinner(
                "📰 Fetching latest news..."
            ):
                raw_news = get_agri_news(
                    selected_cat
                )
                news_items = parse_news(raw_news)
                st.session_state.news_items = (
                    news_items
                )
                st.session_state.raw_news = raw_news

        st.markdown("<br>", unsafe_allow_html=True)

        # Show news
        if hasattr(st.session_state, 'news_items'):
            items = st.session_state.news_items

            if items:
                for news in items:
                    importance = news.get(
                        'importance', 'Medium'
                    )
                    imp_color = (
                        "#C62828"
                        if importance == "High"
                        else "#FF6F00"
                        if importance == "Medium"
                        else "#2E7D32"
                    )
                    imp_bg = (
                        "#FFEBEE"
                        if importance == "High"
                        else "#FFF8E1"
                        if importance == "Medium"
                        else "#E8F5E9"
                    )

                    st.markdown(f"""
                    <div class="news-card">
                        <div style="
                            display:flex;
                            justify-content:
                                space-between;
                            align-items:flex-start;
                            margin-bottom:10px;
                        ">
                            <div style="
                                font-size:17px;
                                font-weight:700;
                                color:#1B5E20;
                                flex:1;
                                margin-right:12px;
                            ">
                                📰 {news.get(
                                    'title', 'News'
                                )}
                            </div>
                            <div style="
                                background:{imp_bg};
                                color:{imp_color};
                                border-radius:8px;
                                padding:4px 10px;
                                font-size:12px;
                                font-weight:700;
                                white-space:nowrap;
                            ">
                                {importance}
                            </div>
                        </div>
                        <div style="
                            font-size:14px;
                            color:#555;
                            line-height:1.7;
                            margin-bottom:10px;
                        ">
                            {news.get(
                                'summary', ''
                            )}
                        </div>
                        {
                            f'<div style="'
                            f'background:#E8F5E9;'
                            f'border-radius:8px;'
                            f'padding:8px 12px;'
                            f'font-size:13px;'
                            f'color:#1B5E20;'
                            f'font-weight:500;">'
                            f'✅ Action: '
                            f'{news.get("action","")}'
                            f'</div>'
                            if news.get('action')
                            else ''
                        }
                        <div class="news-date"
                             style="margin-top:8px;">
                            📅 {news.get('date', '')}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                # Show raw if parsing fails
                st.markdown(f"""
                <div class="result-box">
                    <div style="
                        font-size:14px;
                        color:#333;
                        line-height:1.9;
                        white-space:pre-wrap;
                    ">
                        {st.session_state.raw_news}
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="
                text-align:center;
                padding:50px;
                color:#888;
                background:#F9F9F9;
                border-radius:16px;
            ">
                <div style="font-size:60px;">
                    📰
                </div>
                <div style="
                    font-size:16px;
                    margin-top:12px;
                ">
                    Click 'Load Latest News'
                    to get updates!
                </div>
            </div>
            """, unsafe_allow_html=True)

    # ==========================
    #   TAB 2 - GOVT SCHEMES
    # ==========================
    with tab2:
        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown("""
        <div style="
            background: linear-gradient(
                135deg, #1B5E20, #FF6F00
            );
            border-radius: 16px;
            padding: 20px;
            color: white;
            margin-bottom: 20px;
            text-align: center;
        ">
            <div style="
                font-family:'Rajdhani',sans-serif;
                font-size:24px;
                font-weight:700;
            ">
                🏛️ Government Schemes for Farmers
            </div>
            <div style="
                font-size:14px;
                opacity:0.9;
                margin-top:6px;
            ">
                Know your rights and benefits!
            </div>
        </div>
        """, unsafe_allow_html=True)

        for scheme in GOVT_SCHEMES:
            st.markdown(f"""
            <div class="card" style="
                border-color:{scheme['color']};
            ">
                <div style="
                    display:flex;
                    align-items:center;
                    gap:16px;
                    margin-bottom:12px;
                ">
                    <div style="
                        font-size:40px;
                    ">
                        {scheme['emoji']}
                    </div>
                    <div>
                        <div style="
                            font-size:20px;
                            font-weight:700;
                            color:{scheme['color']};
                        ">
                            {scheme['name']}
                        </div>
                    </div>
                </div>
                <div style="
                    display:flex;
                    gap:8px;
                    flex-wrap:wrap;
                    margin-bottom:10px;
                ">
                    <span style="
                        background:#E8F5E9;
                        color:#2E7D32;
                        padding:4px 12px;
                        border-radius:20px;
                        font-size:13px;
                        font-weight:600;
                    ">
                        💰 {scheme['benefit']}
                    </span>
                </div>
                <div style="
                    font-size:13px;
                    color:#555;
                    margin-bottom:8px;
                ">
                    👤 Who: {scheme['eligibility']}
                </div>
                <div style="
                    background:#E3F2FD;
                    border-radius:8px;
                    padding:8px 12px;
                    font-size:13px;
                    color:#1565C0;
                    font-weight:500;
                ">
                    📋 How to Apply:
                    {scheme['how_to']}
                </div>
            </div>
            """, unsafe_allow_html=True)

    # ==========================
    # TAB 3 - SEASONAL ADVISORY
    # ==========================
    with tab3:
        st.markdown("<br>", unsafe_allow_html=True)

        month = datetime.datetime.now().month
        month_name = datetime.datetime.now().strftime(
            "%B"
        )

        # Season detection
        if month in [6, 7, 8, 9]:
            season = "Kharif"
            season_emoji = "🌧️"
            season_color = "#1565C0"
        elif month in [10, 11, 12, 1, 2, 3]:
            season = "Rabi"
            season_emoji = "❄️"
            season_color = "#6A1B9A"
        else:
            season = "Zaid"
            season_emoji = "☀️"
            season_color = "#E65100"

        st.markdown(f"""
        <div style="
            background: linear-gradient(
                135deg,
                {season_color},
                {season_color}99
            );
            border-radius: 20px;
            padding: 28px;
            color: white;
            text-align: center;
            margin-bottom: 24px;
        ">
            <div style="font-size:60px;">
                {season_emoji}
            </div>
            <div style="
                font-family:'Rajdhani',sans-serif;
                font-size:32px;
                font-weight:700;
                margin-top:8px;
            ">
                {season} Season Advisory
            </div>
            <div style="
                font-size:16px;
                opacity:0.9;
                margin-top:6px;
            ">
                {month_name} Farming Guide
            </div>
        </div>
        """, unsafe_allow_html=True)

        if st.button(
            f"🌾 Get {month_name} Advisory",
            use_container_width=True
        ):
            with st.spinner(
                "Generating advisory..."
            ):
                model = genai.GenerativeModel(
                    "gemini-1.5-flash"
                )
                prompt = f"""
                Give a detailed farming advisory
                for Indian farmers for
                {month_name} during {season} season.

                Include:
                1. WEATHER OUTLOOK
                2. CROPS TO SOW NOW
                3. CROPS TO HARVEST NOW
                4. IRRIGATION TIPS
                5. PEST ALERTS
                6. MARKET TIPS
                7. IMPORTANT TASKS THIS MONTH

                Make it practical for
                Indian farmers.
                Use emojis and clear formatting.
                """
                response = model.generate_content(
                   contents= prompt
                )
                advisory = response.text

            st.markdown(f"""
            <div class="result-box">
                <div style="
                    font-size:14px;
                    color:#333;
                    line-height:1.9;
                    white-space:pre-wrap;
                ">
                    {advisory}
                </div>
            </div>
            """, unsafe_allow_html=True)