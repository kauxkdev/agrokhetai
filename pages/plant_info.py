# =============================================
#      AgroKhet AI - Plant Info Page
# =============================================

import streamlit as st
import google.generativeai as genai
from config import GEMINI_API_KEY

# --- CONFIGURE GEMINI ---
genai.configure(api_key="AIzaSyB0pia4BoKmN9MxANH4USkupHLMeYq8iKY")

# --- PLANT DATABASE ---
PLANTS = {
    "Neem": {
        "emoji": "🌿",
        "hindi": "नीम",
        "type": "Medicinal Tree",
        "uses": [
            "Natural pesticide for crops",
            "Treats skin diseases",
            "Purifies blood",
            "Anti-bacterial properties",
            "Neem oil used in cosmetics"
        ],
        "commercial_value": "Very High",
        "price_range": "₹50-200/kg (leaves)",
        "parts_used": "Leaves, Bark, Seeds, Oil",
        "benefits": [
            "100% organic pesticide",
            "Boosts immunity",
            "Anti-fungal properties",
            "Used in toothpaste industry"
        ],
        "disadvantages": [
            "Bitter taste",
            "Slow growing tree",
            "Seeds toxic if eaten raw"
        ],
        "growing_tips": [
            "Grows in dry conditions",
            "Needs full sunlight",
            "Drought resistant",
            "Grows in almost all soil types"
        ],
        "states": "All India",
        "color": "#2E7D32"
    },
    "Tulsi": {
        "emoji": "🌱",
        "hindi": "तुलसी",
        "type": "Medicinal Herb",
        "uses": [
            "Treats cold and cough",
            "Stress relief",
            "Anti-bacterial herb",
            "Used in Ayurvedic medicine",
            "Religious importance in India"
        ],
        "commercial_value": "High",
        "price_range": "₹30-80/kg",
        "parts_used": "Leaves, Seeds, Oil",
        "benefits": [
            "Boosts immunity",
            "Reduces stress",
            "Anti-inflammatory",
            "Good for respiratory health"
        ],
        "disadvantages": [
            "Needs regular watering",
            "Sensitive to cold weather",
            "Short lifespan (2-3 years)"
        ],
        "growing_tips": [
            "Grow in sunny location",
            "Water daily in summer",
            "Use well-drained soil",
            "Pinch flowers to promote growth"
        ],
        "states": "All India",
        "color": "#1B5E20"
    },
    "Aloe Vera": {
        "emoji": "🪴",
        "hindi": "घृतकुमारी",
        "type": "Medicinal Plant",
        "uses": [
            "Skin care and beauty products",
            "Treats burns and wounds",
            "Digestive health",
            "Hair care products",
            "Cosmetics industry"
        ],
        "commercial_value": "Very High",
        "price_range": "₹15-40/kg (gel)",
        "parts_used": "Gel, Leaves",
        "benefits": [
            "Heals burns quickly",
            "Natural moisturizer",
            "Anti-aging properties",
            "Boosts digestion"
        ],
        "disadvantages": [
            "Latex can cause allergy",
            "Overuse can cause diarrhea",
            "Not suitable for pregnant women"
        ],
        "growing_tips": [
            "Needs very little water",
            "Sandy well-drained soil",
            "Full to partial sunlight",
            "Easy to grow in pots"
        ],
        "states": "Rajasthan, Gujarat, AP",
        "color": "#558B2F"
    },
    "Turmeric": {
        "emoji": "🟡",
        "hindi": "हल्दी",
        "type": "Spice Crop",
        "uses": [
            "Cooking spice",
            "Medicinal properties",
            "Natural dye",
            "Cosmetics ingredient",
            "Religious ceremonies"
        ],
        "commercial_value": "Very High",
        "price_range": "₹100-160/kg",
        "parts_used": "Rhizome (root)",
        "benefits": [
            "Anti-inflammatory",
            "Antioxidant properties",
            "Boosts immunity",
            "Good for liver health"
        ],
        "disadvantages": [
            "Stains everything yellow",
            "Can cause acidity in excess",
            "Needs lots of water"
        ],
        "growing_tips": [
            "Plant rhizomes in June-July",
            "Needs warm humid climate",
            "Partial shade is beneficial",
            "Harvest at 8-9 months"
        ],
        "states": "Telangana, Tamil Nadu, Karnataka",
        "color": "#F9A825"
    },
    "Ashwagandha": {
        "emoji": "🌾",
        "hindi": "अश्वगंधा",
        "type": "Medicinal Herb",
        "uses": [
            "Stress and anxiety relief",
            "Boosts energy and stamina",
            "Improves sleep quality",
            "Used in Ayurvedic medicine",
            "Supplements industry"
        ],
        "commercial_value": "Very High",
        "price_range": "₹200-500/kg",
        "parts_used": "Roots, Leaves, Seeds",
        "benefits": [
            "Reduces cortisol levels",
            "Improves brain function",
            "Anti-cancer properties",
            "High demand globally"
        ],
        "disadvantages": [
            "Not safe during pregnancy",
            "Can cause drowsiness",
            "Bitter taste"
        ],
        "growing_tips": [
            "Grows in dry sandy soil",
            "Drought resistant crop",
            "Harvest roots at 6 months",
            "Low water requirement"
        ],
        "states": "MP, Rajasthan, UP, Gujarat",
        "color": "#FF6F00"
    },
    "Banana": {
        "emoji": "🍌",
        "hindi": "केला",
        "type": "Fruit Crop",
        "uses": [
            "Fresh fruit consumption",
            "Chips and snacks",
            "Banana flour",
            "Fiber from stem",
            "Leaves used as plates"
        ],
        "commercial_value": "High",
        "price_range": "₹15-40/dozen",
        "parts_used": "Fruit, Flower, Stem, Leaves",
        "benefits": [
            "High potassium content",
            "Quick energy source",
            "Good for digestion",
            "Year round availability"
        ],
        "disadvantages": [
            "Needs lots of water",
            "Susceptible to Panama wilt",
            "Fruits bruise easily"
        ],
        "growing_tips": [
            "Plant suckers in June-July",
            "Regular irrigation needed",
            "Support stem when fruiting",
            "Harvest at 12-15 months"
        ],
        "states": "Tamil Nadu, AP, Maharashtra, UP",
        "color": "#F9A825"
    },
    "Sandalwood": {
        "emoji": "🪵",
        "hindi": "चंदन",
        "type": "Commercial Tree",
        "uses": [
            "Perfume and fragrance",
            "Religious purposes",
            "Ayurvedic medicine",
            "Cosmetics and soaps",
            "Wood carving"
        ],
        "commercial_value": "Extremely High",
        "price_range": "₹6000-10000/kg",
        "parts_used": "Heartwood, Oil",
        "benefits": [
            "Most expensive wood in India",
            "Long lasting fragrance",
            "Anti-septic properties",
            "High export demand"
        ],
        "disadvantages": [
            "Takes 15-20 years to mature",
            "Government regulations apply",
            "Needs specific climate",
            "Prone to spike disease"
        ],
        "growing_tips": [
            "Needs host plant nearby",
            "Semi-arid climate ideal",
            "Well-drained rocky soil",
            "Karnataka is best state"
        ],
        "states": "Karnataka, Tamil Nadu, AP",
        "color": "#795548"
    },
    "Bamboo": {
        "emoji": "🎋",
        "hindi": "बांस",
        "type": "Commercial Plant",
        "uses": [
            "Construction material",
            "Furniture making",
            "Paper production",
            "Food (bamboo shoots)",
            "Handicrafts"
        ],
        "commercial_value": "High",
        "price_range": "₹30-100/piece",
        "parts_used": "Stem, Shoots, Leaves",
        "benefits": [
            "Fastest growing plant",
            "Carbon sequestration",
            "Prevents soil erosion",
            "Multiple harvests possible"
        ],
        "disadvantages": [
            "Spreads aggressively",
            "Flowers once then dies",
            "Not suitable for small land"
        ],
        "growing_tips": [
            "Plant in rainy season",
            "Needs well-drained soil",
            "Harvest after 3-4 years",
            "Cut every 2-3 years"
        ],
        "states": "Assam, NE India, Karnataka",
        "color": "#33691E"
    },
}

# --- AI PLANT SEARCH ---
def search_plant_ai(query):
    try:
        model = genai.GenerativeModel(
            "gemini-2.5-flash"
        )
        prompt = f"""
        Give detailed information about this
        plant/tree/herb: {query}

        Include:
        1. COMMON NAME & HINDI NAME
        2. TYPE (Medicinal/Commercial/Food/etc)
        3. MAIN USES (5 points)
        4. BENEFITS (5 points)
        5. DISADVANTAGES (3 points)
        6. COMMERCIAL VALUE
        7. PRICE RANGE in India (INR)
        8. GROWING TIPS (4 points)
        9. BEST STATES IN INDIA
        10. PARTS USED

        Make it practical and useful for
        Indian farmers.
        Format clearly with numbers and labels.
        """
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"❌ Search failed: {str(e)}"

# --- MAIN SHOW FUNCTION ---
def show():

    user = st.session_state.user

    # --- NAVBAR ---
    st.markdown(f"""
    <div class="navbar">
        <div class="navbar-brand">🌾 AgroKhet AI</div>
        <div class="navbar-user">
            🌳 Plant Info | 👤 {user['full_name']}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # --- HEADER ---
    st.markdown("""
    <div class="section-header">
        🌳 Plant & Tree Information
    </div>
    """, unsafe_allow_html=True)

    # --- TABS ---
    tab1, tab2 = st.tabs([
        "🌿 Plant Database",
        "🔍 AI Plant Search"
    ])

    # ==========================
    #   TAB 1 - PLANT DATABASE
    # ==========================
    with tab1:
        st.markdown("<br>", unsafe_allow_html=True)

        # Search bar
        search = st.text_input(
            "🔍 Search Plant",
            placeholder="Type plant name..."
        )

        # Filter
        filtered = {
            k: v for k, v in PLANTS.items()
            if search.lower() in k.lower()
            or search.lower() in v['hindi'].lower()
        } if search else PLANTS

        # Plant type filter
        plant_types = list(set(
            v['type'] for v in PLANTS.values()
        ))
        selected_type = st.selectbox(
            "Filter by Type",
            ["All Types"] + plant_types
        )

        if selected_type != "All Types":
            filtered = {
                k: v for k, v in filtered.items()
                if v['type'] == selected_type
            }

        st.markdown("<br>", unsafe_allow_html=True)

        # Plant cards
        for i in range(0, len(filtered), 2):
            cols = st.columns(2)
            plants_list = list(filtered.items())

            for j, col in enumerate(cols):
                if i + j < len(plants_list):
                    name, data = plants_list[i + j]

                    with col:
                        with st.expander(
                            f"{data['emoji']} "
                            f"{name} "
                            f"({data['hindi']})",
                            expanded=False
                        ):
                            # Header
                            st.markdown(f"""
                            <div style="
                                background: linear-gradient(
                                    135deg,
                                    {data['color']},
                                    {data['color']}99
                                );
                                border-radius: 16px;
                                padding: 20px;
                                color: white;
                                text-align: center;
                                margin-bottom: 16px;
                            ">
                                <div style="
                                    font-size:48px;
                                ">
                                    {data['emoji']}
                                </div>
                                <div style="
                                    font-size:24px;
                                    font-weight:700;
                                    font-family:
                                        'Rajdhani',sans-serif;
                                ">
                                    {name}
                                </div>
                                <div style="
                                    font-size:18px;
                                    opacity:0.9;
                                ">
                                    {data['hindi']}
                                </div>
                                <div style="
                                    font-size:13px;
                                    opacity:0.7;
                                    margin-top:6px;
                                ">
                                    {data['type']}
                                </div>
                            </div>
                            """, unsafe_allow_html=True)

                            # Details
                            col_a, col_b = st.columns(2)

                            with col_a:
                                st.markdown(f"""
                                <div class="card"
                                     style="padding:12px;">
                                    <div style="
                                        font-size:12px;
                                        color:#888;
                                    ">
                                        💰 Commercial Value
                                    </div>
                                    <div style="
                                        font-size:16px;
                                        font-weight:700;
                                        color:#2E7D32;
                                    ">
                                        {data[
                                            'commercial_value'
                                        ]}
                                    </div>
                                </div>
                                """,
                                unsafe_allow_html=True)

                            with col_b:
                                st.markdown(f"""
                                <div class="card"
                                     style="
                                     padding:12px;
                                     border-color:#FF6F00;">
                                    <div style="
                                        font-size:12px;
                                        color:#888;
                                    ">
                                        💵 Price Range
                                    </div>
                                    <div style="
                                        font-size:14px;
                                        font-weight:700;
                                        color:#FF6F00;
                                    ">
                                        {data['price_range']}
                                    </div>
                                </div>
                                """,
                                unsafe_allow_html=True)

                            # Uses
                            st.markdown(
                                "**✅ Main Uses:**"
                            )
                            for use in data['uses']:
                                st.markdown(
                                    f"• {use}"
                                )

                            # Benefits
                            st.markdown(
                                "**💚 Benefits:**"
                            )
                            for b in data['benefits']:
                                st.markdown(f"• {b}")

                            # Disadvantages
                            st.markdown(
                                "**⚠️ Disadvantages:**"
                            )
                            for d in data[
                                'disadvantages'
                            ]:
                                st.markdown(f"• {d}")

                            # Growing tips
                            st.markdown(
                                "**🌱 Growing Tips:**"
                            )
                            for tip in data[
                                'growing_tips'
                            ]:
                                st.markdown(
                                    f"• {tip}"
                                )

                            st.markdown(f"""
                            <div style="
                                background:#E8F5E9;
                                border-radius:10px;
                                padding:10px;
                                font-size:13px;
                                color:#1B5E20;
                                margin-top:10px;
                            ">
                                📍 Best States:
                                {data['states']}<br>
                                🌿 Parts Used:
                                {data['parts_used']}
                            </div>
                            """, unsafe_allow_html=True)

    # ==========================
    #   TAB 2 - AI PLANT SEARCH
    # ==========================
    with tab2:
        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown("""
        <div style="
            background: #E8F5E9;
            border-radius: 16px;
            padding: 20px;
            margin-bottom: 20px;
            border-left: 5px solid #2E7D32;
        ">
            <div style="
                font-size:16px;
                font-weight:600;
                color:#1B5E20;
            ">
                🤖 AI Plant Search
            </div>
            <div style="
                font-size:14px;
                color:#555;
                margin-top:8px;
            ">
                Search any plant, tree, herb or crop
                not in our database.
                AI will give you complete information!
            </div>
        </div>
        """, unsafe_allow_html=True)

        query = st.text_input(
            "🔍 Enter Plant Name",
            placeholder=(
                "e.g. Moringa, Stevia, "
                "Lavender, Giloy..."
            )
        )

        if st.button(
            "🔍 Search with AI",
            use_container_width=True
        ):
            if not query:
                st.error(
                    "❌ Please enter a plant name!"
                )
            else:
                with st.spinner(
                    f"🤖 Searching info for "
                    f"{query}..."
                ):
                    result = search_plant_ai(query)

                st.markdown("""
                <div class="section-header">
                    📋 Plant Information
                </div>
                """, unsafe_allow_html=True)

                st.markdown(f"""
                <div class="result-box">
                    <div style="
                        font-size:14px;
                        color:#333;
                        line-height:1.9;
                        white-space:pre-wrap;
                    ">
                        {result}
                    </div>
                </div>
                """, unsafe_allow_html=True)

        # Popular searches
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("""
        <div style="
            font-size:15px;
            font-weight:600;
            color:#1B5E20;
            margin-bottom:12px;
        ">
            🔥 Popular Searches:
        </div>
        """, unsafe_allow_html=True)

        popular = [
            "Moringa", "Giloy", "Stevia",
            "Lavender", "Amla", "Brahmi",
            "Lemongrass", "Marigold"
        ]

        cols = st.columns(4)
        for i, plant in enumerate(popular):
            with cols[i % 4]:
                if st.button(
                    f"🌿 {plant}",
                    use_container_width=True,
                    key=f"pop_{plant}"
                ):
                    with st.spinner(
                        f"Searching {plant}..."
                    ):
                        result = search_plant_ai(
                            plant
                        )
                    st.markdown(f"""
                    <div class="result-box">
                        <div style="
                            font-size:14px;
                            color:#333;
                            line-height:1.9;
                            white-space:pre-wrap;
                        ">
                            {result}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)