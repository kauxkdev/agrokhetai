# =============================================
#        AgroKhet AI - AgroBot Page
# =============================================

import streamlit as st
import google.generativeai as genai
from config import GEMINI_API_KEY, LANGUAGES
from deep_translator import GoogleTranslator
from gtts import gTTS
import os
import time

# --- CONFIGURE GEMINI ---
genai.configure(api_key="AIzaSyB0pia4BoKmN9MxANH4USkupHLMeYq8iKY")

# --- TRANSLATE TEXT ---
def translate_text(text, target_lang):
    if target_lang == "en":
        return text
    try:
        return GoogleTranslator(
            source="en",
            target=target_lang
        ).translate(text[:4000])
    except:
        return text

# --- ASK AGROBOT ---
def ask_agrobot(question, language_code, history):
    try:
        model = genai.GenerativeModel(
            "gemini-2.5-flash"
        )

        # Build conversation history
        history_text = ""
        for msg in history[-6:]:
            role = msg['role']
            content = msg['content']
            history_text += (
                f"{role}: {content}\n"
            )

        prompt = f"""
        You are AgroBot, an expert AI assistant
        for Indian farmers created by AgroKhet AI.

        You help farmers with:
        - Crop diseases and treatments
        - Weather and irrigation advice
        - Market prices and selling tips
        - Soil health and fertilizers
        - Government schemes for farmers
        - Organic farming techniques
        - Pest control methods
        - Crop selection and planning

        Always give practical, actionable advice
        suitable for Indian farmers.
        Keep answers clear and simple.
        Use relevant emojis to make it friendly.

        Previous conversation:
        {history_text}

        Farmer's question: {question}

        Give a helpful, practical answer.
        """

        response = model.generate_content(prompt)
        answer = response.text

        # Translate if needed
        if language_code != "en":
            answer = translate_text(
                answer, language_code
            )

        return answer

    except Exception as e:
        return f"❌ Error: {str(e)}"

# --- TEXT TO SPEECH ---
def speak_text(text, lang_code):
    try:
        clean = text[:500]
        tts = gTTS(text=clean, lang=lang_code)
        audio_file = "assets/bot_audio.mp3"
        tts.save(audio_file)
        return audio_file
    except:
        return None

# --- MAIN SHOW FUNCTION ---
def show():

    user = st.session_state.user
    lang = st.session_state.language
    lang_code = LANGUAGES.get(lang, "en")

    # --- NAVBAR ---
    st.markdown(f"""
    <div class="navbar">
        <div class="navbar-brand">🌾 AgroKhet AI</div>
        <div class="navbar-user">
            🤖 AgroBot | 👤 {user['full_name']}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # --- HEADER ---
    st.markdown("""
    <div class="section-header">
        🤖 AgroBot - Your AI Farming Assistant
    </div>
    """, unsafe_allow_html=True)

    # --- BOT INTRO ---
    st.markdown("""
    <div style="
        background: linear-gradient(
            135deg, #1B5E20, #2E7D32
        );
        border-radius: 20px;
        padding: 24px;
        color: white;
        margin-bottom: 24px;
        display: flex;
        align-items: center;
        gap: 20px;
    ">
        <div style="font-size:60px;">🤖</div>
        <div>
            <div style="
                font-family:'Rajdhani',sans-serif;
                font-size:24px;
                font-weight:700;
            ">
                Hello! I am AgroBot 👋
            </div>
            <div style="
                font-size:14px;
                opacity:0.9;
                margin-top:6px;
                line-height:1.6;
            ">
                I can help you with crop diseases,
                weather advice, market prices,
                soil health, government schemes
                and all farming questions!
                Ask me anything in your language! 🌾
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # --- INITIALIZE CHAT HISTORY ---
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # --- LANGUAGE SELECTOR ---
    col1, col2 = st.columns([2, 1])

    with col1:
        selected_lang = st.selectbox(
            "🌐 Chat Language",
            list(LANGUAGES.keys()),
            index=list(
                LANGUAGES.keys()
            ).index(lang)
        )
        lang_code = LANGUAGES[selected_lang]

    with col2:
        if st.button(
            "🗑️ Clear Chat",
            use_container_width=True
        ):
            st.session_state.chat_history = []
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # --- QUICK QUESTIONS ---
    st.markdown("""
    <div style="
        font-size:15px;
        font-weight:600;
        color:#1B5E20;
        margin-bottom:12px;
    ">
        ⚡ Quick Questions:
    </div>
    """, unsafe_allow_html=True)

    quick_questions = [
        "🌿 How to treat yellow leaves?",
        "💧 How often to water wheat?",
        "🐛 How to remove pests organically?",
        "💰 When to sell crops for best price?",
        "🌱 Best crop for my soil?",
        "📋 What govt schemes for farmers?",
        "🌧️ Effect of rain on crops?",
        "🧪 Which fertilizer is best?"
    ]

    cols = st.columns(4)
    for i, q in enumerate(quick_questions):
        with cols[i % 4]:
            if st.button(
                q,
                use_container_width=True,
                key=f"quick_{i}"
            ):
                with st.spinner(
                    "🤖 AgroBot is thinking..."
                ):
                    answer = ask_agrobot(
                        q, lang_code,
                        st.session_state.chat_history
                    )
                st.session_state.chat_history.append(
                    {"role": "Farmer", "content": q}
                )
                st.session_state.chat_history.append(
                    {"role": "AgroBot",
                     "content": answer}
                )
                st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # --- CHAT DISPLAY ---
    st.markdown("""
    <div style="
        font-size:16px;
        font-weight:600;
        color:#1B5E20;
        margin-bottom:12px;
    ">
        💬 Chat History
    </div>
    """, unsafe_allow_html=True)

    # Show chat messages
    chat_container = st.container()

    with chat_container:
        if st.session_state.chat_history:
            for msg in st.session_state.chat_history:
                if msg['role'] == "Farmer":
                    st.markdown(f"""
                    <div style="
                        display:flex;
                        justify-content:flex-end;
                        margin-bottom:12px;
                    ">
                        <div class="chat-message-user">
                            <div style="
                                font-size:11px;
                                opacity:0.7;
                                margin-bottom:4px;
                            ">
                                👤 You
                            </div>
                            {msg['content']}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div style="
                        display:flex;
                        justify-content:flex-start;
                        margin-bottom:12px;
                    ">
                        <div class="chat-message-bot">
                            <div style="
                                font-size:11px;
                                color:#FF6F00;
                                font-weight:600;
                                margin-bottom:4px;
                            ">
                                🤖 AgroBot
                            </div>
                            {msg['content']}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="
                text-align:center;
                padding:40px;
                color:#888;
                background:#F9F9F9;
                border-radius:16px;
            ">
                <div style="font-size:48px;">
                    🤖
                </div>
                <div style="
                    font-size:16px;
                    margin-top:12px;
                ">
                    Ask me anything about farming!
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # --- INPUT BOX ---
    st.markdown("""
    <div style="
        font-size:15px;
        font-weight:600;
        color:#1B5E20;
        margin-bottom:8px;
    ">
        ✍️ Ask AgroBot:
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([4, 1])

    with col1:
        user_input = st.text_input(
            "Your question",
            placeholder=(
                "Ask anything about farming, "
                "crops, weather, prices..."
            ),
            label_visibility="collapsed"
        )

    with col2:
        send = st.button(
            "📨 Send",
            use_container_width=True
        )

    if send and user_input:
        with st.spinner(
            "🤖 AgroBot is thinking..."
        ):
            answer = ask_agrobot(
                user_input,
                lang_code,
                st.session_state.chat_history
            )

        st.session_state.chat_history.append(
            {"role": "Farmer",
             "content": user_input}
        )
        st.session_state.chat_history.append(
            {"role": "AgroBot",
             "content": answer}
        )
        st.rerun()

    # --- VOICE OUTPUT ---
    if st.session_state.chat_history:
        last_bot = None
        for msg in reversed(
            st.session_state.chat_history
        ):
            if msg['role'] == "AgroBot":
                last_bot = msg['content']
                break

        if last_bot:
            if st.button(
                "🔊 Listen to Last Answer",
                use_container_width=True
            ):
                with st.spinner(
                    "Generating audio..."
                ):
                    audio = speak_text(
                        last_bot, lang_code
                    )
                    if audio and os.path.exists(
                        audio
                    ):
                        st.audio(audio)
                    else:
                        st.warning(
                            "⚠️ Voice not available "
                            "for this language"
                        )

    st.markdown("<br>", unsafe_allow_html=True)

    # --- AGROBOT CAPABILITIES ---
    st.markdown("""
    <div class="section-header">
        💡 What AgroBot Can Help With
    </div>
    """, unsafe_allow_html=True)

    capabilities = [
        ("🌿", "Crop Diseases",
         "Identify and treat crop diseases"),
        ("💧", "Irrigation",
         "Water schedule and tips"),
        ("🐛", "Pest Control",
         "Organic and chemical solutions"),
        ("💰", "Market Prices",
         "Best time and place to sell"),
        ("🌱", "Crop Selection",
         "Best crop for your land"),
        ("📋", "Govt Schemes",
         "PM Kisan, subsidies and more"),
        ("🧪", "Fertilizers",
         "Which fertilizer and when"),
        ("🌾", "Harvesting",
         "Best time and methods"),
    ]

    cap_cols = st.columns(4)
    for i, (emoji, title, desc) in enumerate(
        capabilities
    ):
        with cap_cols[i % 4]:
            st.markdown(f"""
            <div class="card"
                 style="text-align:center;
                 padding:16px;">
                <div style="font-size:32px;">
                    {emoji}
                </div>
                <div style="
                    font-size:14px;
                    font-weight:600;
                    color:#1B5E20;
                    margin-top:8px;
                ">
                    {title}
                </div>
                <div style="
                    font-size:12px;
                    color:#888;
                    margin-top:4px;
                ">
                    {desc}
                </div>
            </div>
            """, unsafe_allow_html=True)