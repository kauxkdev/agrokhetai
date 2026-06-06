# =============================================
#        AgroKhet AI - My Farm Page
# =============================================

import streamlit as st
import plotly.graph_objects as go
import datetime
from database import (
    save_farm,
    get_farm_data,
    get_scan_history
)

# --- MAIN SHOW FUNCTION ---
def show():

    user = st.session_state.user

    # --- NAVBAR ---
    st.markdown(f"""
    <div class="navbar">
        <div class="navbar-brand">🌾 AgroKhet AI</div>
        <div class="navbar-user">
            🚜 My Farm | 👤 {user['full_name']}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # --- HEADER ---
    st.markdown("""
    <div class="section-header">
        🚜 My Farm Dashboard
    </div>
    """, unsafe_allow_html=True)

    # --- TABS ---
    tab1, tab2, tab3 = st.tabs([
        "🌾 My Crops",
        "📊 Scan History",
        "👤 My Profile"
    ])

    # ==========================
    #     TAB 1 - MY CROPS
    # ==========================
    with tab1:
        st.markdown("<br>", unsafe_allow_html=True)

        # Add new crop form
        st.markdown("""
        <div class="section-header"
             style="font-size:20px;">
            ➕ Add New Crop
        </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns(2)

        with col1:
            crop_name = st.text_input(
                "🌾 Crop Name",
                placeholder="e.g. Wheat, Rice..."
            )
            land_size = st.text_input(
                "📏 Land Size",
                placeholder="e.g. 2 Acres"
            )
            sow_date = st.date_input(
                "🌱 Sowing Date",
                value=datetime.date.today()
            )

        with col2:
            harvest_date = st.date_input(
                "🌾 Expected Harvest Date",
                value=(
                    datetime.date.today() +
                    datetime.timedelta(days=120)
                )
            )
            notes = st.text_area(
                "📝 Notes",
                placeholder=(
                    "Any special notes about "
                    "this crop..."
                ),
                height=120
            )

        if st.button(
            "➕ Add Crop to My Farm",
            use_container_width=True
        ):
            if not crop_name or not land_size:
                st.error(
                    "❌ Please fill crop name "
                    "and land size!"
                )
            else:
                save_farm(
                    user_id=user['id'],
                    crop_name=crop_name,
                    land_size=land_size,
                    sow_date=str(sow_date),
                    harvest_date=str(harvest_date),
                    notes=notes
                )
                st.success(
                    f"✅ {crop_name} added to "
                    f"your farm!"
                )
                st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)

        # Show existing crops
        st.markdown("""
        <div class="section-header"
             style="font-size:20px;">
            🌾 My Current Crops
        </div>
        """, unsafe_allow_html=True)

        farm_data = get_farm_data(user['id'])

        if farm_data:
            for crop in farm_data:
                # Calculate days remaining
                try:
                    harvest = datetime.datetime\
                        .strptime(
                            crop['harvest_date'],
                            "%Y-%m-%d"
                        ).date()
                    today = datetime.date.today()
                    days_left = (harvest - today).days
                    if days_left > 0:
                        status = (
                            f"🌱 {days_left} days "
                            f"to harvest"
                        )
                        status_color = "#2E7D32"
                    else:
                        status = "🌾 Ready to Harvest!"
                        status_color = "#FF6F00"
                except:
                    status = "📅 Check dates"
                    status_color = "#888"

                st.markdown(f"""
                <div class="card">
                    <div style="
                        display:flex;
                        justify-content:space-between;
                        align-items:flex-start;
                    ">
                        <div>
                            <div style="
                                font-size:22px;
                                font-weight:700;
                                color:#1B5E20;
                            ">
                                🌾 {crop['crop_name']}
                            </div>
                            <div style="
                                font-size:14px;
                                color:#888;
                                margin-top:4px;
                            ">
                                📏 {crop['land_size']}
                            </div>
                        </div>
                        <div style="
                            background:{status_color};
                            color:white;
                            border-radius:10px;
                            padding:8px 14px;
                            font-size:13px;
                            font-weight:600;
                        ">
                            {status}
                        </div>
                    </div>
                    <div style="
                        margin-top:14px;
                        display:flex;
                        gap:20px;
                        flex-wrap:wrap;
                    ">
                        <div style="
                            font-size:13px;
                            color:#555;
                        ">
                            🌱 Sown:
                            {crop['sow_date']}
                        </div>
                        <div style="
                            font-size:13px;
                            color:#555;
                        ">
                            🌾 Harvest:
                            {crop['harvest_date']}
                        </div>
                    </div>
                    {
                        f'<div style="font-size:13px;'
                        f'color:#888;margin-top:8px;">'
                        f'📝 {crop["notes"]}</div>'
                        if crop['notes'] else ''
                    }
                </div>
                """, unsafe_allow_html=True)

            # Farm summary chart
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("""
            <div class="section-header"
                 style="font-size:20px;">
                📊 Farm Overview
            </div>
            """, unsafe_allow_html=True)

            crop_names = [
                c['crop_name'] for c in farm_data
            ]
            crop_counts = [1] * len(crop_names)

            fig = go.Figure(data=[
                go.Pie(
                    labels=crop_names,
                    values=crop_counts,
                    hole=0.4,
                    marker=dict(
                        colors=[
                            '#2E7D32', '#FF6F00',
                            '#1565C0', '#F9A825',
                            '#6A1B9A', '#C62828'
                        ]
                    )
                )
            ])

            fig.update_layout(
                title="🌾 My Crops Distribution",
                height=350,
                plot_bgcolor='white',
                paper_bgcolor='white',
                font=dict(family="Poppins"),
                title_font=dict(
                    size=16,
                    color='#1B5E20'
                )
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        else:
            st.markdown("""
            <div style="
                text-align:center;
                padding:50px;
                color:#888;
            ">
                <div style="font-size:60px;">
                    🌾
                </div>
                <div style="
                    font-size:18px;
                    margin-top:12px;
                ">
                    No crops added yet!
                    Add your first crop above.
                </div>
            </div>
            """, unsafe_allow_html=True)

    # ==========================
    #   TAB 2 - SCAN HISTORY
    # ==========================
    with tab2:
        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown("""
        <div class="section-header"
             style="font-size:20px;">
            🔍 My Crop Scan History
        </div>
        """, unsafe_allow_html=True)

        scans = get_scan_history(user['id'])

        if scans:
            # Stats
            col1, col2 = st.columns(2)

            with col1:
                st.markdown(f"""
                <div class="card">
                    <div class="card-icon">🔬</div>
                    <div class="card-title">
                        Total Scans
                    </div>
                    <div class="card-value">
                        {len(scans)}
                    </div>
                </div>
                """, unsafe_allow_html=True)

            with col2:
                st.markdown(f"""
                <div class="card"
                     style="border-color:#FF6F00;">
                    <div class="card-icon">📅</div>
                    <div class="card-title">
                        Last Scan
                    </div>
                    <div style="
                        font-size:16px;
                        font-weight:600;
                        color:#FF6F00;
                        margin-top:8px;
                    ">
                        {scans[0]['scanned_at']
                            [:10]
                            if scans else 'N/A'}
                    </div>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            # Scan cards
            for scan in scans:
                st.markdown(f"""
                <div class="card"
                     style="border-color:#C62828;">
                    <div style="
                        display:flex;
                        justify-content:space-between;
                        align-items:center;
                    ">
                        <div>
                            <div style="
                                font-size:18px;
                                font-weight:700;
                                color:#C62828;
                            ">
                                🦠 {scan['disease_name']}
                            </div>
                            <div style="
                                font-size:13px;
                                color:#888;
                                margin-top:4px;
                            ">
                                📅 {scan['scanned_at'][:10]}
                            </div>
                        </div>
                        <div style="
                            background:#FFEBEE;
                            color:#C62828;
                            border-radius:10px;
                            padding:6px 12px;
                            font-size:12px;
                            font-weight:600;
                        ">
                            {scan['confidence']}
                        </div>
                    </div>
                    <div style="
                        font-size:13px;
                        color:#555;
                        margin-top:10px;
                        line-height:1.6;
                    ">
                        {scan['treatment'][:200]}...
                    </div>
                </div>
                """, unsafe_allow_html=True)

        else:
            st.markdown("""
            <div style="
                text-align:center;
                padding:50px;
                color:#888;
            ">
                <div style="font-size:60px;">
                    🔬
                </div>
                <div style="
                    font-size:18px;
                    margin-top:12px;
                ">
                    No scans yet!
                    Go to Crop Scanner to start.
                </div>
            </div>
            """, unsafe_allow_html=True)

            if st.button(
                "🌿 Go to Crop Scanner",
                use_container_width=True
            ):
                st.session_state.page = (
                    "crop_scanner"
                )
                st.rerun()

    # ==========================
    #    TAB 3 - MY PROFILE
    # ==========================
    with tab3:
        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown("""
        <div class="section-header"
             style="font-size:20px;">
            👤 My Profile
        </div>
        """, unsafe_allow_html=True)

        # Profile card
        st.markdown(f"""
        <div style="
            background: linear-gradient(
                135deg, #1B5E20, #FF6F00
            );
            border-radius: 24px;
            padding: 32px;
            color: white;
            text-align: center;
            margin-bottom: 24px;
        ">
            <div style="
                font-size: 80px;
            ">
                👨‍🌾
            </div>
            <div style="
                font-family:'Rajdhani',sans-serif;
                font-size: 32px;
                font-weight: 700;
                margin-top: 12px;
            ">
                {user['full_name']}
            </div>
            <div style="
                font-size: 16px;
                opacity: 0.9;
                margin-top: 6px;
            ">
                📍 {user['state']}
            </div>
            <div style="
                font-size: 14px;
                opacity: 0.7;
                margin-top: 4px;
            ">
                🌐 {user['language']}
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Profile details
        details = [
            ("👤 Full Name", user['full_name']),
            ("📧 Email", user['email']),
            ("📱 Phone", user['phone']),
            ("📍 State", user['state']),
            ("🌐 Language", user['language']),
            ("📅 Member Since",
             str(user['created_at'])[:10]),
        ]

        for label, value in details:
            st.markdown(f"""
            <div style="
                background: white;
                border-radius: 12px;
                padding: 16px 20px;
                margin-bottom: 10px;
                border-left: 4px solid #2E7D32;
                box-shadow: 0 2px 8px
                    rgba(0,0,0,0.06);
                display: flex;
                justify-content: space-between;
                align-items: center;
            ">
                <div style="
                    font-size: 14px;
                    color: #888;
                    font-weight: 500;
                ">
                    {label}
                </div>
                <div style="
                    font-size: 15px;
                    font-weight: 600;
                    color: #1B5E20;
                ">
                    {value}
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Logout button
        if st.button(
            "🚪 Logout from Account",
            use_container_width=True
        ):
            st.session_state.user = None
            st.session_state.page = "auth"
            st.rerun()