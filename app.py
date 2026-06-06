# =============================================
#         AgroKhet AI - Main Entry Point
# =============================================

import streamlit as st
import time
from database import create_tables
from config import APP_NAME, APP_TAGLINE, COLORS

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="AgroKhet AI",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- LOAD CSS ---
def load_css():
    try:
        with open("assets/styles.css") as f:
            st.markdown(
                f"<style>{f.read()}</style>",
                unsafe_allow_html=True
            )
    except:
        pass

load_css()

# --- INITIALIZE DATABASE ---
create_tables()

# --- INITIALIZE SESSION STATE ---
if "page" not in st.session_state:
    st.session_state.page = "splash"

if "user" not in st.session_state:
    st.session_state.user = None

if "language" not in st.session_state:
    st.session_state.language = "English"

if "splash_done" not in st.session_state:
    st.session_state.splash_done = False

if "prev_page" not in st.session_state:
    st.session_state.prev_page = "home"


# --- SPLASH SCREEN ---
def show_splash():
    st.markdown("""
    <div class="splash-container">
        <div style="font-size:100px;">🌾</div>
        <div class="splash-title">AgroKhet AI</div>
        <div class="splash-tagline">
            Smart Farming, Better Future
        </div>
        <div style="color:#FFF8E1;
                    font-size:13px;
                    margin-top:8px;
                    opacity:0.7;">
            Powered by Gemini AI
        </div>
        <div class="splash-loader">
            <div class="splash-loader-bar"></div>
        </div>
        <div style="color:#C8E6C9;
                    font-size:12px;
                    margin-top:20px;
                    opacity:0.6;">
            Loading your smart farm assistant...
        </div>
    </div>
    """, unsafe_allow_html=True)
    time.sleep(3)
    st.session_state.splash_done = True
    st.session_state.page = "auth"
    st.rerun()


# --- TOP-OF-PAGE BACK BUTTON ---
def show_top_back_button(page_title: str = ""):
    """
    Shows a styled back-to-home button at the top of any non-home page.
    Call this at the very start of show_main_app() page rendering,
    AFTER the sidebar is built.
    """
    col_btn, col_title, col_space = st.columns([1.2, 5, 1.2])

    with col_btn:
        if st.button(
            "⬅️ Home",
            key="top_back_btn",
            use_container_width=True,
            help="Go back to Home"
        ):
            st.session_state.prev_page = st.session_state.page
            st.session_state.page = "home"
            st.rerun()

    with col_title:
        if page_title:
            st.markdown(
                f"""
                <div style="
                    font-size:20px;
                    font-weight:700;
                    color:#2E7D32;
                    padding-top:6px;
                    font-family:'Rajdhani',sans-serif;
                ">
                    {page_title}
                </div>
                """,
                unsafe_allow_html=True
            )

    # Divider below the top bar
    st.markdown(
        "<hr style='margin-top:4px; margin-bottom:16px; border-color:#E0E0E0;'>",
        unsafe_allow_html=True
    )


# --- PAGE TITLE MAP ---
PAGE_TITLES = {
    "crop_scanner":  "🌿 Crop Scanner",
    "weather":       "🌦️ Weather",
    "market":        "💰 Market Price",
    "crop_calendar": "📅 Crop Calendar",
    "water_land":    "💧 Water & Land",
    "plant_info":    "🌳 Plant Info",
    "my_farm":       "🚜 My Farm",
    "agrobot":       "🤖 AgroBot",
    "news":          "📰 News",
}


# --- MAIN APP AFTER LOGIN ---
def show_main_app():

    from pages import (
        home, crop_scanner,
        weather, market,
        crop_calendar, water_land,
        plant_info, my_farm,
        agrobot, news
    )

    # --- SIDEBAR ---
    with st.sidebar:

        # Logo and name
        st.markdown(f"""
        <div style="text-align:center;
                    padding:20px 0;">
            <div style="font-size:50px;">🌾</div>
            <div style="
                font-family:'Rajdhani',sans-serif;
                font-size:24px;
                font-weight:700;
                color:#2E7D32;">
                AgroKhet AI
            </div>
            <div style="
                font-size:13px;
                color:#888;
                margin-top:4px;">
                👤 {st.session_state.user['full_name']}
            </div>
        </div>
        <hr style="border-color:#E0E0E0;">
        """, unsafe_allow_html=True)

        # --- SIDEBAR BACK BUTTON ---
        # Only show when NOT on home page
        if st.session_state.page != "home":
            if st.button(
                "⬅️ Back to Home",
                use_container_width=True,
                key="sidebar_back_btn"
            ):
                st.session_state.prev_page = (
                    st.session_state.page
                )
                st.session_state.page = "home"
                st.rerun()

            st.markdown(
                "<hr style='border-color:#E0E0E0;'>",
                unsafe_allow_html=True
            )

        # --- NAV MENU ---
        pages = {
            "🏠 Home": "home",
            "🌿 Crop Scanner": "crop_scanner",
            "🌦️ Weather": "weather",
            "💰 Market Price": "market",
            "📅 Crop Calendar": "crop_calendar",
            "💧 Water & Land": "water_land",
            "🌳 Plant Info": "plant_info",
            "🚜 My Farm": "my_farm",
            "🤖 AgroBot": "agrobot",
            "📰 News": "news",
        }

        for label, page_key in pages.items():
            is_current = (
                st.session_state.page == page_key
            )

            # Highlight active page
            if is_current:
                st.markdown(f"""
                <div style="
                    background:linear-gradient(
                        135deg,#2E7D32,#FF6F00
                    );
                    border-radius:10px;
                    padding:10px 16px;
                    color:white;
                    font-weight:600;
                    font-size:14px;
                    margin-bottom:4px;
                ">
                    {label} ◀
                </div>
                """, unsafe_allow_html=True)
            else:
                if st.button(
                    label,
                    key=f"nav_{page_key}",
                    use_container_width=True
                ):
                    st.session_state.prev_page = (
                        st.session_state.page
                    )
                    st.session_state.page = page_key
                    st.rerun()

        st.markdown(
            "<hr style='border-color:#E0E0E0;'>",
            unsafe_allow_html=True
        )

        # --- LOGOUT ---
        if st.button(
            "🚪 Logout",
            use_container_width=True
        ):
            st.session_state.user = None
            st.session_state.page = "auth"
            st.rerun()

    # --- LOAD PAGE ---
    page = st.session_state.page

    if page == "home":
        home.show()

    else:
        # ✅ Show top back button on every non-home page
        show_top_back_button(
            PAGE_TITLES.get(page, "")
        )

        if page == "crop_scanner":
            crop_scanner.show()
        elif page == "weather":
            weather.show()
        elif page == "market":
            market.show()
        elif page == "crop_calendar":
            crop_calendar.show()
        elif page == "water_land":
            water_land.show()
        elif page == "plant_info":
            plant_info.show()
        elif page == "my_farm":
            my_farm.show()
        elif page == "agrobot":
            agrobot.show()
        elif page == "news":
            news.show()


# --- MAIN ROUTER ---
def main():
    page = st.session_state.page

    if page == "splash" and \
            not st.session_state.splash_done:
        show_splash()

    elif page == "auth" or \
            st.session_state.user is None:
        from pages import auth
        auth.show()

    else:
        show_main_app()


if __name__ == "__main__":
    main()