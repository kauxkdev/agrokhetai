# =============================================
#      AgroKhet AI - Crop Calendar Page
# =============================================

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px

# --- CROP CALENDAR DATABASE ---
CROP_CALENDAR = {
    "Wheat": {
        "emoji": "🌾",
        "season": "Rabi",
        "sow_months": ["October", "November"],
        "harvest_months": ["March", "April"],
        "duration_days": 120,
        "states": "Punjab, Haryana, UP, MP",
        "profit": "High",
        "investment": "Medium",
        "water_need": "Medium",
        "temp_range": "15-25°C",
        "soil": "Loamy, Clay",
        "yield_per_acre": "15-20 Quintals",
        "price_range": "₹2100-2400/Quintal",
        "tips": [
            "Sow in October-November for best results",
            "Use certified seeds for higher yield",
            "Apply irrigation at crown root stage",
            "Watch for rust disease in February"
        ]
    },
    "Rice": {
        "emoji": "🍚",
        "season": "Kharif",
        "sow_months": ["June", "July"],
        "harvest_months": ["October", "November"],
        "duration_days": 130,
        "states": "Punjab, WB, AP, Tamil Nadu",
        "profit": "High",
        "investment": "High",
        "water_need": "Very High",
        "temp_range": "25-35°C",
        "soil": "Clay, Waterlogged",
        "yield_per_acre": "18-25 Quintals",
        "price_range": "₹1900-2500/Quintal",
        "tips": [
            "Transplant seedlings at 25-30 days",
            "Maintain 5cm water level in field",
            "Apply fertilizer in 3 splits",
            "Watch for blast disease in monsoon"
        ]
    },
    "Cotton": {
        "emoji": "🌸",
        "season": "Kharif",
        "sow_months": ["April", "May", "June"],
        "harvest_months": [
            "October", "November", "December"
        ],
        "duration_days": 180,
        "states": "Gujarat, Maharashtra, AP, Punjab",
        "profit": "Very High",
        "investment": "High",
        "water_need": "Medium",
        "temp_range": "25-35°C",
        "soil": "Black, Loamy",
        "yield_per_acre": "8-15 Quintals",
        "price_range": "₹5500-7000/Quintal",
        "tips": [
            "Use Bt cotton for pest resistance",
            "Avoid waterlogging in fields",
            "Spray for bollworm in August",
            "Pick cotton in dry weather only"
        ]
    },
    "Soybean": {
        "emoji": "🫘",
        "season": "Kharif",
        "sow_months": ["June", "July"],
        "harvest_months": ["September", "October"],
        "duration_days": 100,
        "states": "MP, Maharashtra, Rajasthan",
        "profit": "Medium",
        "investment": "Low",
        "water_need": "Low",
        "temp_range": "20-30°C",
        "soil": "Well-drained Loamy",
        "yield_per_acre": "8-12 Quintals",
        "price_range": "₹4000-5200/Quintal",
        "tips": [
            "Treat seeds with Rhizobium culture",
            "Avoid water stress at pod filling",
            "Harvest when 95% pods turn brown",
            "Good option for crop rotation"
        ]
    },
    "Maize": {
        "emoji": "🌽",
        "season": "Kharif",
        "sow_months": ["June", "July"],
        "harvest_months": [
            "September", "October"
        ],
        "duration_days": 90,
        "states": "Karnataka, Bihar, AP, UP",
        "profit": "Medium",
        "investment": "Medium",
        "water_need": "Medium",
        "temp_range": "20-30°C",
        "soil": "Loamy, Sandy Loam",
        "yield_per_acre": "20-30 Quintals",
        "price_range": "₹1700-2200/Quintal",
        "tips": [
            "Plant in rows for better yield",
            "Apply nitrogen in 3 splits",
            "Irrigate at tasseling stage",
            "Harvest when grain moisture is 25%"
        ]
    },
    "Mustard": {
        "emoji": "🌻",
        "season": "Rabi",
        "sow_months": ["October", "November"],
        "harvest_months": ["February", "March"],
        "duration_days": 110,
        "states": "Rajasthan, UP, Haryana, MP",
        "profit": "High",
        "investment": "Low",
        "water_need": "Low",
        "temp_range": "10-25°C",
        "soil": "Loamy, Sandy Loam",
        "yield_per_acre": "6-10 Quintals",
        "price_range": "₹4800-6000/Quintal",
        "tips": [
            "Sow in rows for easy harvesting",
            "One irrigation at flowering stage",
            "Watch for aphids in January",
            "Harvest when 75% pods turn yellow"
        ]
    },
    "Tomato": {
        "emoji": "🍅",
        "season": "Rabi/Zaid",
        "sow_months": [
            "September", "October", "November"
        ],
        "harvest_months": [
            "December", "January", "February"
        ],
        "duration_days": 90,
        "states": "HP, Karnataka, Maharashtra, AP",
        "profit": "Very High",
        "investment": "High",
        "water_need": "High",
        "temp_range": "20-27°C",
        "soil": "Well-drained Loamy",
        "yield_per_acre": "80-120 Quintals",
        "price_range": "₹400-3000/Quintal",
        "tips": [
            "Use hybrid seeds for better yield",
            "Stake plants at 30cm height",
            "Drip irrigation gives best results",
            "Watch for early blight disease"
        ]
    },
    "Onion": {
        "emoji": "🧅",
        "season": "Rabi",
        "sow_months": [
            "October", "November", "December"
        ],
        "harvest_months": [
            "February", "March", "April"
        ],
        "duration_days": 120,
        "states": "Maharashtra, MP, Karnataka",
        "profit": "High",
        "investment": "Medium",
        "water_need": "Medium",
        "temp_range": "13-24°C",
        "soil": "Loamy, Well-drained",
        "yield_per_acre": "80-100 Quintals",
        "price_range": "₹800-4000/Quintal",
        "tips": [
            "Transplant nursery at 6-8 weeks",
            "Stop irrigation 2 weeks before harvest",
            "Cure bulbs in shade for 2-3 weeks",
            "Store in cool dry ventilated place"
        ]
    },
    "Sugarcane": {
        "emoji": "🎋",
        "season": "Annual",
        "sow_months": [
            "February", "March", "October"
        ],
        "harvest_months": [
            "November", "December",
            "January", "February"
        ],
        "duration_days": 365,
        "states": "UP, Maharashtra, Karnataka, TN",
        "profit": "Medium",
        "investment": "High",
        "water_need": "Very High",
        "temp_range": "21-35°C",
        "soil": "Loamy, Clay Loam",
        "yield_per_acre": "300-400 Quintals",
        "price_range": "₹290-340/Quintal",
        "tips": [
            "Use healthy 3 budded setts",
            "Ratoon crop gives good profit",
            "Earthing up prevents lodging",
            "Harvest at 12 months for best sugar"
        ]
    },
    "Potato": {
        "emoji": "🥔",
        "season": "Rabi",
        "sow_months": ["October", "November"],
        "harvest_months": [
            "January", "February", "March"
        ],
        "duration_days": 90,
        "states": "UP, West Bengal, Punjab, Bihar",
        "profit": "Medium",
        "investment": "Medium",
        "water_need": "Medium",
        "temp_range": "15-25°C",
        "soil": "Sandy Loam, Loamy",
        "yield_per_acre": "80-120 Quintals",
        "price_range": "₹500-1500/Quintal",
        "tips": [
            "Use certified disease-free seeds",
            "Earth up after 30 days of planting",
            "Watch for late blight in cool weather",
            "Store in cold storage for better price"
        ]
    }
}

# --- MONTHS LIST ---
MONTHS = [
    "January", "February", "March",
    "April", "May", "June",
    "July", "August", "September",
    "October", "November", "December"
]

# --- GET CROPS BY MONTH ---
def get_crops_for_month(month):
    sow_crops = []
    harvest_crops = []
    for crop, data in CROP_CALENDAR.items():
        if month in data['sow_months']:
            sow_crops.append((crop, data))
        if month in data['harvest_months']:
            harvest_crops.append((crop, data))
    return sow_crops, harvest_crops

# --- PROFIT COLOR ---
def get_profit_color(profit):
    colors = {
        "Very High": "#1B5E20",
        "High": "#2E7D32",
        "Medium": "#FF6F00",
        "Low": "#C62828"
    }
    return colors.get(profit, "#555")

# --- MAIN SHOW FUNCTION ---
def show():

    user = st.session_state.user

    # --- NAVBAR ---
    st.markdown(f"""
    <div class="navbar">
        <div class="navbar-brand">🌾 AgroKhet AI</div>
        <div class="navbar-user">
            📅 Crop Calendar | 👤 {user['full_name']}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # --- HEADER ---
    st.markdown("""
    <div class="section-header">
        📅 Smart Crop Calendar
    </div>
    """, unsafe_allow_html=True)

    # --- TABS ---
    tab1, tab2, tab3 = st.tabs([
        "📅 Monthly Calendar",
        "🌾 Crop Details",
        "📊 Profit Analysis"
    ])

    # ========================
    #     TAB 1 - CALENDAR
    # ========================
    with tab1:
        st.markdown("<br>", unsafe_allow_html=True)

        # Month selector
        import datetime
        current_month = datetime.datetime.now().strftime(
            "%B"
        )
        selected_month = st.selectbox(
            "📅 Select Month",
            MONTHS,
            index=MONTHS.index(current_month)
        )

        sow_crops, harvest_crops = get_crops_for_month(
            selected_month
        )

        col1, col2 = st.columns(2)

        # SOWING CROPS
        with col1:
            st.markdown(f"""
            <div style="
                background: linear-gradient(
                    135deg, #1B5E20, #2E7D32
                );
                border-radius: 16px;
                padding: 20px;
                color: white;
                margin-bottom: 16px;
            ">
                <div style="
                    font-size:22px;
                    font-weight:700;
                    font-family:'Rajdhani',sans-serif;
                ">
                    🌱 Sow in {selected_month}
                </div>
                <div style="
                    font-size:13px;
                    opacity:0.8;
                    margin-top:4px;
                ">
                    Best crops to plant this month
                </div>
            </div>
            """, unsafe_allow_html=True)

            if sow_crops:
                for crop, data in sow_crops:
                    profit_color = get_profit_color(
                        data['profit']
                    )
                    st.markdown(f"""
                    <div class="card">
                        <div style="
                            display:flex;
                            align-items:center;
                            gap:12px;
                        ">
                            <div style="font-size:36px;">
                                {data['emoji']}
                            </div>
                            <div>
                                <div style="
                                    font-size:18px;
                                    font-weight:700;
                                    color:#1B5E20;
                                ">
                                    {crop}
                                </div>
                                <div style="
                                    font-size:13px;
                                    color:#888;
                                ">
                                    {data['season']} Season
                                </div>
                            </div>
                        </div>
                        <div style="
                            margin-top:12px;
                            display:flex;
                            gap:8px;
                            flex-wrap:wrap;
                        ">
                            <span style="
                                background:#E8F5E9;
                                color:#2E7D32;
                                padding:4px 10px;
                                border-radius:20px;
                                font-size:12px;
                                font-weight:600;
                            ">
                                💰 {data['profit']} Profit
                            </span>
                            <span style="
                                background:#FFF8E1;
                                color:#FF6F00;
                                padding:4px 10px;
                                border-radius:20px;
                                font-size:12px;
                                font-weight:600;
                            ">
                                💧 {data['water_need']} Water
                            </span>
                            <span style="
                                background:#E3F2FD;
                                color:#1565C0;
                                padding:4px 10px;
                                border-radius:20px;
                                font-size:12px;
                                font-weight:600;
                            ">
                                ⏱️ {data['duration_days']} Days
                            </span>
                        </div>
                        <div style="
                            font-size:13px;
                            color:#888;
                            margin-top:10px;
                        ">
                            📍 {data['states']}
                        </div>
                        <div style="
                            font-size:13px;
                            color:#2E7D32;
                            font-weight:600;
                            margin-top:6px;
                        ">
                            🌾 Yield: {data['yield_per_acre']}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div style="
                    text-align:center;
                    padding:30px;
                    color:#888;
                ">
                    😔 No major crops to sow this month
                </div>
                """, unsafe_allow_html=True)

        # HARVEST CROPS
        with col2:
            st.markdown(f"""
            <div style="
                background: linear-gradient(
                    135deg, #E65100, #FF6F00
                );
                border-radius: 16px;
                padding: 20px;
                color: white;
                margin-bottom: 16px;
            ">
                <div style="
                    font-size:22px;
                    font-weight:700;
                    font-family:'Rajdhani',sans-serif;
                ">
                    🌾 Harvest in {selected_month}
                </div>
                <div style="
                    font-size:13px;
                    opacity:0.8;
                    margin-top:4px;
                ">
                    Crops ready to harvest this month
                </div>
            </div>
            """, unsafe_allow_html=True)

            if harvest_crops:
                for crop, data in harvest_crops:
                    st.markdown(f"""
                    <div class="card"
                         style="border-color:#FF6F00;">
                        <div style="
                            display:flex;
                            align-items:center;
                            gap:12px;
                        ">
                            <div style="font-size:36px;">
                                {data['emoji']}
                            </div>
                            <div>
                                <div style="
                                    font-size:18px;
                                    font-weight:700;
                                    color:#E65100;
                                ">
                                    {crop}
                                </div>
                                <div style="
                                    font-size:13px;
                                    color:#888;
                                ">
                                    Ready to Harvest! 🎉
                                </div>
                            </div>
                        </div>
                        <div style="
                            margin-top:12px;
                            font-size:14px;
                            color:#555;
                        ">
                            💰 Price: {data['price_range']}
                        </div>
                        <div style="
                            font-size:13px;
                            color:#888;
                            margin-top:6px;
                        ">
                            📍 Best Market: {data['states']}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div style="
                    text-align:center;
                    padding:30px;
                    color:#888;
                ">
                    😔 No major crops to harvest
                    this month
                </div>
                """, unsafe_allow_html=True)

    # ========================
    #   TAB 2 - CROP DETAILS
    # ========================
    with tab2:
        st.markdown("<br>", unsafe_allow_html=True)

        selected_crop = st.selectbox(
            "🌾 Select Crop for Details",
            list(CROP_CALENDAR.keys())
        )

        if selected_crop:
            data = CROP_CALENDAR[selected_crop]

            # Header
            st.markdown(f"""
            <div style="
                background: linear-gradient(
                    135deg, #1B5E20, #FF6F00
                );
                border-radius: 20px;
                padding: 28px;
                color: white;
                margin-bottom: 24px;
            ">
                <div style="font-size:60px;">
                    {data['emoji']}
                </div>
                <div style="
                    font-family:'Rajdhani',sans-serif;
                    font-size:36px;
                    font-weight:700;
                ">
                    {selected_crop}
                </div>
                <div style="
                    font-size:16px;
                    opacity:0.9;
                    margin-top:8px;
                ">
                    {data['season']} Season Crop
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Details grid
            col1, col2 = st.columns(2)

            with col1:
                details = [
                    ("🌱 Sow Months",
                     ", ".join(data['sow_months'])),
                    ("🌾 Harvest Months",
                     ", ".join(data['harvest_months'])),
                    ("⏱️ Duration",
                     f"{data['duration_days']} days"),
                    ("🌡️ Temperature",
                     data['temp_range']),
                    ("🏔️ Soil Type", data['soil']),
                ]
                for label, value in details:
                    st.markdown(f"""
                    <div style="
                        background:white;
                        border-radius:12px;
                        padding:14px 18px;
                        margin-bottom:10px;
                        border-left:4px solid #2E7D32;
                        box-shadow:0 2px 8px
                            rgba(0,0,0,0.06);
                    ">
                        <div style="
                            font-size:13px;
                            color:#888;
                        ">
                            {label}
                        </div>
                        <div style="
                            font-size:16px;
                            font-weight:600;
                            color:#1B5E20;
                            margin-top:4px;
                        ">
                            {value}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

            with col2:
                details2 = [
                    ("💰 Profit Level",
                     data['profit']),
                    ("💸 Investment",
                     data['investment']),
                    ("💧 Water Need",
                     data['water_need']),
                    ("🌾 Yield/Acre",
                     data['yield_per_acre']),
                    ("💵 Price Range",
                     data['price_range']),
                ]
                for label, value in details2:
                    st.markdown(f"""
                    <div style="
                        background:white;
                        border-radius:12px;
                        padding:14px 18px;
                        margin-bottom:10px;
                        border-left:4px solid #FF6F00;
                        box-shadow:0 2px 8px
                            rgba(0,0,0,0.06);
                    ">
                        <div style="
                            font-size:13px;
                            color:#888;
                        ">
                            {label}
                        </div>
                        <div style="
                            font-size:16px;
                            font-weight:600;
                            color:#E65100;
                            margin-top:4px;
                        ">
                            {value}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

            # Tips
            st.markdown("""
            <div class="section-header">
                💡 Expert Farming Tips
            </div>
            """, unsafe_allow_html=True)

            for tip in data['tips']:
                st.markdown(f"""
                <div style="
                    background:#E8F5E9;
                    border-radius:12px;
                    padding:14px 20px;
                    margin-bottom:10px;
                    border-left:4px solid #2E7D32;
                    font-size:15px;
                    color:#1B5E20;
                    font-weight:500;
                ">
                    ✅ {tip}
                </div>
                """, unsafe_allow_html=True)

    # ========================
    #  TAB 3 - PROFIT ANALYSIS
    # ========================
    with tab3:
        st.markdown("<br>", unsafe_allow_html=True)

        # Profit comparison chart
        crops = list(CROP_CALENDAR.keys())
        profit_map = {
            "Very High": 4,
            "High": 3,
            "Medium": 2,
            "Low": 1
        }
        invest_map = {
            "Very High": 4,
            "High": 3,
            "Medium": 2,
            "Low": 1
        }

        profit_scores = [
            profit_map.get(
                CROP_CALENDAR[c]['profit'], 2
            )
            for c in crops
        ]
        invest_scores = [
            invest_map.get(
                CROP_CALENDAR[c]['investment'], 2
            )
            for c in crops
        ]
        emojis = [
            CROP_CALENDAR[c]['emoji']
            for c in crops
        ]

        fig = go.Figure(data=[
            go.Bar(
                name='Profit Level',
                x=crops,
                y=profit_scores,
                marker_color='#2E7D32',
                text=[
                    CROP_CALENDAR[c]['profit']
                    for c in crops
                ],
                textposition='outside'
            ),
            go.Bar(
                name='Investment Level',
                x=crops,
                y=invest_scores,
                marker_color='#FF6F00',
                text=[
                    CROP_CALENDAR[c]['investment']
                    for c in crops
                ],
                textposition='outside'
            )
        ])

        fig.update_layout(
            title="📊 Profit vs Investment Analysis",
            barmode='group',
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(family="Poppins"),
            title_font=dict(
                size=18,
                color='#1B5E20'
            ),
            height=450,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02
            ),
            xaxis=dict(tickangle=45)
        )

        st.plotly_chart(
            fig, use_container_width=True
        )

        # Best profit crops
        st.markdown("""
        <div class="section-header">
            🏆 Best Profit Crops
        </div>
        """, unsafe_allow_html=True)

        best_crops = [
            (k, v) for k, v in CROP_CALENDAR.items()
            if v['profit'] in ["Very High", "High"]
        ]

        for crop, data in best_crops:
            col1, col2, col3 = st.columns([1, 2, 1])
            with col1:
                st.markdown(f"""
                <div style="
                    font-size:48px;
                    text-align:center;
                ">
                    {data['emoji']}
                </div>
                """, unsafe_allow_html=True)
            with col2:
                st.markdown(f"""
                <div style="padding:8px 0;">
                    <div style="
                        font-size:18px;
                        font-weight:700;
                        color:#1B5E20;
                    ">
                        {crop}
                    </div>
                    <div style="
                        font-size:13px;
                        color:#888;
                        margin-top:4px;
                    ">
                        📍 {data['states']}
                    </div>
                    <div style="
                        font-size:13px;
                        color:#555;
                        margin-top:4px;
                    ">
                        💵 {data['price_range']}
                    </div>
                </div>
                """, unsafe_allow_html=True)
            with col3:
                profit_color = get_profit_color(
                    data['profit']
                )
                st.markdown(f"""
                <div style="
                    background:{profit_color};
                    color:white;
                    border-radius:12px;
                    padding:10px;
                    text-align:center;
                    font-weight:700;
                    font-size:14px;
                ">
                    {data['profit']}<br>Profit
                </div>
                """, unsafe_allow_html=True)
            st.markdown(
                "<hr style='border-color:#E0E0E0;'>",
                unsafe_allow_html=True
            )