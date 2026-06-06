# =============================================
#      AgroKhet AI - Water & Land Page
# =============================================

import streamlit as st
import plotly.graph_objects as go

# --- WATER REQUIREMENT DATABASE ---
WATER_DATA = {
    "Wheat": {
        "emoji": "🌾",
        "total_water_mm": 450,
        "irrigations": 5,
        "critical_stages": [
            "Crown Root (20-25 days)",
            "Tillering (40-45 days)",
            "Jointing (60-65 days)",
            "Flowering (80-85 days)",
            "Grain Filling (100-105 days)"
        ],
        "water_per_acre": "18-20 lakh litres",
        "drip_suitable": False,
        "sprinkler_suitable": True,
    },
    "Rice": {
        "emoji": "🍚",
        "total_water_mm": 1200,
        "irrigations": 20,
        "critical_stages": [
            "Transplanting (0 days)",
            "Tillering (15-30 days)",
            "Panicle Initiation (55 days)",
            "Flowering (75-80 days)",
            "Grain Filling (85-100 days)"
        ],
        "water_per_acre": "50-60 lakh litres",
        "drip_suitable": False,
        "sprinkler_suitable": False,
    },
    "Cotton": {
        "emoji": "🌸",
        "total_water_mm": 700,
        "irrigations": 8,
        "critical_stages": [
            "Germination (0-10 days)",
            "Square Formation (45 days)",
            "Flowering (60-70 days)",
            "Boll Development (90 days)",
            "Boll Opening (120 days)"
        ],
        "water_per_acre": "28-32 lakh litres",
        "drip_suitable": True,
        "sprinkler_suitable": False,
    },
    "Tomato": {
        "emoji": "🍅",
        "total_water_mm": 600,
        "irrigations": 15,
        "critical_stages": [
            "Transplanting (0 days)",
            "Vegetative Growth (15-30 days)",
            "Flowering (35-45 days)",
            "Fruit Setting (50-60 days)",
            "Fruit Development (65-80 days)"
        ],
        "water_per_acre": "24-28 lakh litres",
        "drip_suitable": True,
        "sprinkler_suitable": True,
    },
    "Maize": {
        "emoji": "🌽",
        "total_water_mm": 500,
        "irrigations": 6,
        "critical_stages": [
            "Germination (0-7 days)",
            "Knee High (30 days)",
            "Tasseling (50-55 days)",
            "Silking (55-60 days)",
            "Grain Filling (65-80 days)"
        ],
        "water_per_acre": "20-22 lakh litres",
        "drip_suitable": True,
        "sprinkler_suitable": True,
    },
    "Soybean": {
        "emoji": "🫘",
        "total_water_mm": 450,
        "irrigations": 4,
        "critical_stages": [
            "Germination (0-7 days)",
            "Vegetative (20-30 days)",
            "Flowering (40-50 days)",
            "Pod Filling (60-70 days)",
            "Maturity (90-100 days)"
        ],
        "water_per_acre": "18-20 lakh litres",
        "drip_suitable": True,
        "sprinkler_suitable": True,
    },
    "Mustard": {
        "emoji": "🌻",
        "total_water_mm": 300,
        "irrigations": 3,
        "critical_stages": [
            "Germination (0-7 days)",
            "Branching (25-30 days)",
            "Flowering (45-50 days)",
        ],
        "water_per_acre": "12-14 lakh litres",
        "drip_suitable": False,
        "sprinkler_suitable": True,
    },
    "Sugarcane": {
        "emoji": "🎋",
        "total_water_mm": 1500,
        "irrigations": 25,
        "critical_stages": [
            "Germination (0-30 days)",
            "Tillering (30-90 days)",
            "Grand Growth (90-270 days)",
            "Maturity (270-365 days)"
        ],
        "water_per_acre": "60-70 lakh litres",
        "drip_suitable": True,
        "sprinkler_suitable": False,
    },
}

# --- SOIL TYPE DATABASE ---
SOIL_DATA = {
    "Sandy Soil": {
        "emoji": "🏜️",
        "color": "#F9A825",
        "water_retention": "Low",
        "drainage": "Very Fast",
        "best_crops": [
            "Groundnut", "Watermelon",
            "Carrot", "Potato"
        ],
        "avoid_crops": ["Rice", "Sugarcane"],
        "ph_range": "6.0 - 7.0",
        "tips": [
            "Add organic matter to improve water retention",
            "Irrigate more frequently",
            "Good for root vegetables",
            "Use drip irrigation for best results"
        ]
    },
    "Clay Soil": {
        "emoji": "🟫",
        "color": "#795548",
        "water_retention": "Very High",
        "drainage": "Very Slow",
        "best_crops": [
            "Rice", "Wheat",
            "Sugarcane", "Cotton"
        ],
        "avoid_crops": ["Groundnut", "Carrot"],
        "ph_range": "5.5 - 7.0",
        "tips": [
            "Add sand and organic matter for drainage",
            "Avoid waterlogging",
            "Good for water-intensive crops",
            "Till deeply before sowing"
        ]
    },
    "Loamy Soil": {
        "emoji": "🌱",
        "color": "#2E7D32",
        "water_retention": "Medium",
        "drainage": "Good",
        "best_crops": [
            "Wheat", "Maize", "Vegetables",
            "Fruits", "Cotton", "Soybean"
        ],
        "avoid_crops": [],
        "ph_range": "6.0 - 7.5",
        "tips": [
            "Best soil for most crops",
            "Maintain organic matter levels",
            "Regular crop rotation recommended",
            "Suitable for all irrigation types"
        ]
    },
    "Black Soil": {
        "emoji": "⬛",
        "color": "#212121",
        "water_retention": "High",
        "drainage": "Slow",
        "best_crops": [
            "Cotton", "Soybean",
            "Wheat", "Sunflower"
        ],
        "avoid_crops": ["Rice"],
        "ph_range": "7.5 - 8.5",
        "tips": [
            "Famous as cotton soil in India",
            "Rich in calcium and magnesium",
            "Cracks in dry season - normal",
            "Add gypsum to reduce alkalinity"
        ]
    },
    "Red Soil": {
        "emoji": "🔴",
        "color": "#C62828",
        "water_retention": "Low",
        "drainage": "Fast",
        "best_crops": [
            "Groundnut", "Millets",
            "Tobacco", "Potato"
        ],
        "avoid_crops": ["Rice", "Sugarcane"],
        "ph_range": "5.5 - 6.5",
        "tips": [
            "Low in nitrogen and phosphorus",
            "Add lime to correct acidity",
            "Good for drought-resistant crops",
            "Use organic manure regularly"
        ]
    },
    "Alluvial Soil": {
        "emoji": "💧",
        "color": "#1565C0",
        "water_retention": "Medium-High",
        "drainage": "Good",
        "best_crops": [
            "Rice", "Wheat", "Sugarcane",
            "Maize", "Vegetables"
        ],
        "avoid_crops": [],
        "ph_range": "6.5 - 7.5",
        "tips": [
            "Most fertile soil in India",
            "Found in Indo-Gangetic plains",
            "Good for almost all crops",
            "Regular fertilization needed"
        ]
    },
}

# --- MAIN SHOW FUNCTION ---
def show():

    user = st.session_state.user

    # --- NAVBAR ---
    st.markdown(f"""
    <div class="navbar">
        <div class="navbar-brand">🌾 AgroKhet AI</div>
        <div class="navbar-user">
            💧 Water & Land | 👤 {user['full_name']}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # --- HEADER ---
    st.markdown("""
    <div class="section-header">
        💧 Water & Land Management
    </div>
    """, unsafe_allow_html=True)

    # --- TABS ---
    tab1, tab2, tab3 = st.tabs([
        "💧 Water Calculator",
        "🌍 Soil Guide",
        "📅 Irrigation Schedule"
    ])

    # ===========================
    #   TAB 1 - WATER CALCULATOR
    # ===========================
    with tab1:
        st.markdown("<br>", unsafe_allow_html=True)

        col1, col2 = st.columns(2)

        with col1:
            crop = st.selectbox(
                "🌾 Select Your Crop",
                list(WATER_DATA.keys())
            )
            land_size = st.number_input(
                "📏 Land Size (in Acres)",
                min_value=0.5,
                max_value=100.0,
                value=1.0,
                step=0.5
            )
            soil_type = st.selectbox(
                "🌍 Your Soil Type",
                list(SOIL_DATA.keys())
            )

        with col2:
            if crop:
                data = WATER_DATA[crop]

                st.markdown(f"""
                <div style="
                    background: linear-gradient(
                        135deg, #1565C0, #42A5F5
                    );
                    border-radius: 20px;
                    padding: 24px;
                    color: white;
                    text-align: center;
                ">
                    <div style="font-size:48px;">
                        {data['emoji']}
                    </div>
                    <div style="
                        font-family:'Rajdhani',sans-serif;
                        font-size:28px;
                        font-weight:700;
                        margin-top:8px;
                    ">
                        {crop} Water Needs
                    </div>
                    <div style="
                        font-size:42px;
                        font-weight:700;
                        color:#FFF9C4;
                        margin-top:12px;
                    ">
                        {data['total_water_mm']} mm
                    </div>
                    <div style="
                        font-size:14px;
                        opacity:0.8;
                        margin-top:4px;
                    ">
                        Total water needed
                    </div>
                    <div style="
                        font-size:18px;
                        margin-top:16px;
                        font-weight:600;
                    ">
                        💧 {data['irrigations']}
                        irrigations needed
                    </div>
                    <div style="
                        font-size:14px;
                        opacity:0.8;
                        margin-top:8px;
                    ">
                        Per acre: {data['water_per_acre']}
                    </div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        if crop:
            data = WATER_DATA[crop]

            # Total water for land size
            total_irrigations = (
                data['irrigations'] * land_size
            )

            # Stats
            col1, col2, col3 = st.columns(3)

            with col1:
                st.markdown(f"""
                <div class="card">
                    <div class="card-icon">💧</div>
                    <div class="card-title">
                        Total Irrigations
                    </div>
                    <div class="card-value">
                        {data['irrigations']}
                    </div>
                    <div style="
                        font-size:12px;
                        color:#888;
                    ">
                        For full crop cycle
                    </div>
                </div>
                """, unsafe_allow_html=True)

            with col2:
                drip = "✅ Yes" if data[
                    'drip_suitable'
                ] else "❌ No"
                st.markdown(f"""
                <div class="card"
                     style="border-color:#1565C0;">
                    <div class="card-icon">🚿</div>
                    <div class="card-title">
                        Drip Irrigation
                    </div>
                    <div style="
                        font-size:24px;
                        font-weight:700;
                        color:#1565C0;
                        margin-top:8px;
                    ">
                        {drip}
                    </div>
                </div>
                """, unsafe_allow_html=True)

            with col3:
                sprinkler = "✅ Yes" if data[
                    'sprinkler_suitable'
                ] else "❌ No"
                st.markdown(f"""
                <div class="card"
                     style="border-color:#FF6F00;">
                    <div class="card-icon">💦</div>
                    <div class="card-title">
                        Sprinkler Irrigation
                    </div>
                    <div style="
                        font-size:24px;
                        font-weight:700;
                        color:#FF6F00;
                        margin-top:8px;
                    ">
                        {sprinkler}
                    </div>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            # Critical stages
            st.markdown("""
            <div class="section-header">
                ⚠️ Critical Irrigation Stages
            </div>
            """, unsafe_allow_html=True)

            for i, stage in enumerate(
                data['critical_stages']
            ):
                st.markdown(f"""
                <div style="
                    background: white;
                    border-radius: 12px;
                    padding: 14px 20px;
                    margin-bottom: 10px;
                    border-left: 4px solid #1565C0;
                    display: flex;
                    align-items: center;
                    gap: 12px;
                    box-shadow: 0 2px 8px
                        rgba(0,0,0,0.06);
                ">
                    <div style="
                        background: #1565C0;
                        color: white;
                        width: 28px;
                        height: 28px;
                        border-radius: 50%;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        font-weight: 700;
                        font-size: 14px;
                        flex-shrink: 0;
                    ">
                        {i+1}
                    </div>
                    <div style="
                        font-size: 15px;
                        color: #1B5E20;
                        font-weight: 500;
                    ">
                        💧 {stage}
                    </div>
                </div>
                """, unsafe_allow_html=True)

    # ===========================
    #    TAB 2 - SOIL GUIDE
    # ===========================
    with tab2:
        st.markdown("<br>", unsafe_allow_html=True)

        selected_soil = st.selectbox(
            "🌍 Select Your Soil Type",
            list(SOIL_DATA.keys())
        )

        if selected_soil:
            soil = SOIL_DATA[selected_soil]

            # Soil header
            st.markdown(f"""
            <div style="
                background: linear-gradient(
                    135deg,
                    {soil['color']},
                    {soil['color']}99
                );
                border-radius: 20px;
                padding: 28px;
                color: white;
                margin-bottom: 24px;
                text-align: center;
            ">
                <div style="font-size:60px;">
                    {soil['emoji']}
                </div>
                <div style="
                    font-family:'Rajdhani',sans-serif;
                    font-size:32px;
                    font-weight:700;
                    margin-top:8px;
                ">
                    {selected_soil}
                </div>
                <div style="
                    font-size:16px;
                    opacity:0.9;
                    margin-top:8px;
                ">
                    pH Range: {soil['ph_range']}
                </div>
            </div>
            """, unsafe_allow_html=True)

            col1, col2 = st.columns(2)

            with col1:
                st.markdown(f"""
                <div class="card">
                    <div class="card-icon">💧</div>
                    <div class="card-title">
                        Water Retention
                    </div>
                    <div class="card-value">
                        {soil['water_retention']}
                    </div>
                </div>
                """, unsafe_allow_html=True)

                st.markdown("""
                <div class="section-header"
                     style="font-size:18px;">
                    ✅ Best Crops
                </div>
                """, unsafe_allow_html=True)

                for crop in soil['best_crops']:
                    st.markdown(f"""
                    <div style="
                        background: #E8F5E9;
                        border-radius: 10px;
                        padding: 10px 16px;
                        margin-bottom: 8px;
                        font-size: 15px;
                        color: #1B5E20;
                        font-weight: 500;
                    ">
                        ✅ {crop}
                    </div>
                    """, unsafe_allow_html=True)

            with col2:
                st.markdown(f"""
                <div class="card"
                     style="border-color:#1565C0;">
                    <div class="card-icon">🚰</div>
                    <div class="card-title">
                        Drainage Speed
                    </div>
                    <div class="card-value"
                         style="color:#1565C0;">
                        {soil['drainage']}
                    </div>
                </div>
                """, unsafe_allow_html=True)

                if soil['avoid_crops']:
                    st.markdown("""
                    <div class="section-header"
                         style="font-size:18px;
                         background:linear-gradient(
                             135deg,#C62828,#E53935
                         );">
                        ❌ Avoid These Crops
                    </div>
                    """, unsafe_allow_html=True)

                    for crop in soil['avoid_crops']:
                        st.markdown(f"""
                        <div style="
                            background: #FFEBEE;
                            border-radius: 10px;
                            padding: 10px 16px;
                            margin-bottom: 8px;
                            font-size: 15px;
                            color: #C62828;
                            font-weight: 500;
                        ">
                            ❌ {crop}
                        </div>
                        """, unsafe_allow_html=True)

            # Tips
            st.markdown("""
            <div class="section-header">
                💡 Soil Management Tips
            </div>
            """, unsafe_allow_html=True)

            for tip in soil['tips']:
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
                    💡 {tip}
                </div>
                """, unsafe_allow_html=True)

    # ===========================
    # TAB 3 - IRRIGATION SCHEDULE
    # ===========================
    with tab3:
        st.markdown("<br>", unsafe_allow_html=True)

        crop = st.selectbox(
            "🌾 Select Crop for Schedule",
            list(WATER_DATA.keys()),
            key="schedule_crop"
        )

        sow_date = st.date_input(
            "📅 Sowing Date"
        )

        if crop and sow_date:
            data = WATER_DATA[crop]

            st.markdown("""
            <div class="section-header">
                📅 Your Irrigation Schedule
            </div>
            """, unsafe_allow_html=True)

            import datetime

            for i, stage in enumerate(
                data['critical_stages']
            ):
                # Extract days from stage name
                try:
                    days_text = stage.split("(")[1]\
                        .split(" ")[0].split("-")[0]
                    days = int(days_text)
                except:
                    days = (i + 1) * 20

                irr_date = (
                    sow_date +
                    datetime.timedelta(days=days)
                )

                st.markdown(f"""
                <div style="
                    background: white;
                    border-radius: 14px;
                    padding: 16px 20px;
                    margin-bottom: 12px;
                    box-shadow: 0 2px 10px
                        rgba(0,0,0,0.06);
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    border-left: 5px solid #1565C0;
                ">
                    <div>
                        <div style="
                            font-size: 16px;
                            font-weight: 600;
                            color: #1B5E20;
                        ">
                            💧 Irrigation {i+1}
                        </div>
                        <div style="
                            font-size: 14px;
                            color: #555;
                            margin-top: 4px;
                        ">
                            {stage}
                        </div>
                    </div>
                    <div style="
                        background: #E3F2FD;
                        border-radius: 10px;
                        padding: 8px 16px;
                        text-align: center;
                    ">
                        <div style="
                            font-size: 18px;
                            font-weight: 700;
                            color: #1565C0;
                        ">
                            {irr_date.strftime(
                                "%d %b %Y"
                            )}
                        </div>
                        <div style="
                            font-size: 12px;
                            color: #888;
                        ">
                            Day {days}
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            st.success(
                f"✅ Schedule ready for {crop}! "
                f"Total {data['irrigations']} "
                f"irrigations needed."
            )