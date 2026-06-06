# =============================================
#         AgroKhet AI - Authentication Page
# =============================================

import streamlit as st
from database import register_user, login_user, update_password, get_user_by_email
from config import LANGUAGES
import random
import time

# --- SHOW AUTH PAGE ---
def show():
    
    # Auth tabs
    if "auth_tab" not in st.session_state:
        st.session_state.auth_tab = "login"

    # --- HEADER ---
    st.markdown("""
    <div style="text-align:center; padding:30px 0 10px 0;">
        <div style="font-size:80px;">🌾</div>
        <div style="font-family:'Rajdhani',sans-serif;
                    font-size:42px;
                    font-weight:700;
                    color:#2E7D32;">
            AgroKhet AI
        </div>
        <div style="font-size:15px;
                    color:#888;
                    margin-top:4px;">
            Smart Farming, Better Future 🚀
        </div>
    </div>
    """, unsafe_allow_html=True)

    # --- CENTER COLUMN ---
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:

        # --- TAB BUTTONS ---
        t1, t2, t3 = st.columns(3)
        with t1:
            if st.button("🔑 Login",
                use_container_width=True):
                st.session_state.auth_tab = "login"
                st.rerun()
        with t2:
            if st.button("📝 Register",
                use_container_width=True):
                st.session_state.auth_tab = "register"
                st.rerun()
        with t3:
            if st.button("🔒 Forgot",
                use_container_width=True):
                st.session_state.auth_tab = "forgot"
                st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)

        # =====================
        #      LOGIN FORM
        # =====================
        if st.session_state.auth_tab == "login":
            st.markdown("""
            <div class="auth-container">
                <div class="auth-title">Welcome Back! 👋</div>
                <div class="auth-subtitle">
                    Login to your AgroKhet account
                </div>
            </div>
            """, unsafe_allow_html=True)

            email = st.text_input(
                "📧 Email Address",
                placeholder="Enter your email"
            )
            password = st.text_input(
                "🔒 Password",
                type="password",
                placeholder="Enter your password"
            )

            st.markdown("<br>", unsafe_allow_html=True)

            if st.button("🚀 Login Now",
                use_container_width=True):
                if not email or not password:
                    st.error("❌ Please fill all fields!")
                else:
                    with st.spinner("Logging in..."):
                        time.sleep(1)
                        success, result = login_user(
                            email, password
                        )
                        if success:
                            st.session_state.user = result
                            st.session_state.language = result.get(
                                'language', 'English'
                            )
                            st.session_state.page = "home"
                            st.success("✅ Login successful!")
                            time.sleep(1)
                            st.rerun()
                        else:
                            st.error(result)

        # =====================
        #    REGISTER FORM
        # =====================
        elif st.session_state.auth_tab == "register":
            st.markdown("""
            <div class="auth-container">
                <div class="auth-title">Join AgroKhet! 🌱</div>
                <div class="auth-subtitle">
                    Create your free account today
                </div>
            </div>
            """, unsafe_allow_html=True)

            full_name = st.text_input(
                "👤 Full Name",
                placeholder="Enter your full name"
            )
            email = st.text_input(
                "📧 Email Address",
                placeholder="Enter your email"
            )
            phone = st.text_input(
                "📱 Phone Number",
                placeholder="Enter your phone number"
            )

            # Indian States
            states = [
                "Select State",
                "Andhra Pradesh", "Arunachal Pradesh",
                "Assam", "Bihar", "Chhattisgarh",
                "Goa", "Gujarat", "Haryana",
                "Himachal Pradesh", "Jharkhand",
                "Karnataka", "Kerala", "Madhya Pradesh",
                "Maharashtra", "Manipur", "Meghalaya",
                "Mizoram", "Nagaland", "Odisha",
                "Punjab", "Rajasthan", "Sikkim",
                "Tamil Nadu", "Telangana", "Tripura",
                "Uttar Pradesh", "Uttarakhand",
                "West Bengal", "Delhi"
            ]
            state = st.selectbox("🗺️ Your State", states)

            language = st.selectbox(
                "🌐 Preferred Language",
                list(LANGUAGES.keys())
            )
            password = st.text_input(
                "🔒 Password",
                type="password",
                placeholder="Create a strong password"
            )
            confirm_password = st.text_input(
                "🔒 Confirm Password",
                type="password",
                placeholder="Repeat your password"
            )

            st.markdown("<br>", unsafe_allow_html=True)

            if st.button("🌱 Create Account",
                use_container_width=True):
                if not all([full_name, email,
                    phone, password,
                    confirm_password]):
                    st.error("❌ Please fill all fields!")
                elif state == "Select State":
                    st.error("❌ Please select your state!")
                elif password != confirm_password:
                    st.error("❌ Passwords do not match!")
                elif len(password) < 6:
                    st.error(
                        "❌ Password must be 6+ characters!"
                    )
                else:
                    with st.spinner("Creating account..."):
                        time.sleep(1)
                        success, message = register_user(
                            full_name, email, phone,
                            password, state, language
                        )
                        if success:
                            st.success(message)
                            st.info(
                                "✅ Now login with your account!"
                            )
                            time.sleep(1)
                            st.session_state.auth_tab = "login"
                            st.rerun()
                        else:
                            st.error(message)

        # =====================
        #    FORGOT PASSWORD
        # =====================
        elif st.session_state.auth_tab == "forgot":
            st.markdown("""
            <div class="auth-container">
                <div class="auth-title">Reset Password 🔐</div>
                <div class="auth-subtitle">
                    Enter your email to reset password
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Step 1 - Enter Email
            if "otp_sent" not in st.session_state:
                st.session_state.otp_sent = False

            if "otp_verified" not in st.session_state:
                st.session_state.otp_verified = False

            if not st.session_state.otp_sent:
                forgot_email = st.text_input(
                    "📧 Registered Email",
                    placeholder="Enter your email"
                )
                if st.button("📨 Send OTP",
                    use_container_width=True):
                    if not forgot_email:
                        st.error("❌ Please enter email!")
                    else:
                        user = get_user_by_email(
                            forgot_email
                        )
                        if user:
                            # Generate OTP
                            otp = str(random.randint(
                                100000, 999999
                            ))
                            st.session_state.reset_otp = otp
                            st.session_state.reset_email = (
                                forgot_email
                            )
                            st.session_state.otp_sent = True
                            st.success(
                                f"✅ Your OTP is: **{otp}**"
                            )
                            st.info(
                                "📋 Copy this OTP and enter below"
                            )
                            st.rerun()
                        else:
                            st.error("❌ Email not found!")

            # Step 2 - Enter OTP
            elif st.session_state.otp_sent and \
                not st.session_state.otp_verified:

                st.success(
                    f"✅ OTP sent for: "
                    f"{st.session_state.reset_email}"
                )
                entered_otp = st.text_input(
                    "🔢 Enter OTP",
                    placeholder="Enter 6 digit OTP"
                )
                if st.button("✅ Verify OTP",
                    use_container_width=True):
                    if entered_otp == st.session_state.reset_otp:
                        st.session_state.otp_verified = True
                        st.rerun()
                    else:
                        st.error("❌ Wrong OTP!")

            # Step 3 - New Password
            elif st.session_state.otp_verified:
                st.success("✅ OTP Verified!")
                new_pass = st.text_input(
                    "🔒 New Password",
                    type="password",
                    placeholder="Enter new password"
                )
                confirm_new = st.text_input(
                    "🔒 Confirm New Password",
                    type="password",
                    placeholder="Repeat new password"
                )
                if st.button("💾 Update Password",
                    use_container_width=True):
                    if not new_pass or not confirm_new:
                        st.error("❌ Please fill both fields!")
                    elif new_pass != confirm_new:
                        st.error("❌ Passwords do not match!")
                    elif len(new_pass) < 6:
                        st.error(
                            "❌ Password must be 6+ characters!"
                        )
                    else:
                        update_password(
                            st.session_state.reset_email,
                            new_pass
                        )
                        st.success("✅ Password updated!")
                        # Reset all states
                        st.session_state.otp_sent = False
                        st.session_state.otp_verified = False
                        st.session_state.auth_tab = "login"
                        time.sleep(1)
                        st.rerun()