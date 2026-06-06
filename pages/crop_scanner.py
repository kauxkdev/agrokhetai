# =============================================
#       AgroKhet AI - Crop Scanner Page
# =============================================

import streamlit as st
import google.generativeai as genai
from PIL import Image
from database import save_scan
from config import GEMINI_API_KEY, LANGUAGES
from deep_translator import GoogleTranslator
from gtts import gTTS
import os
import time
import io

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
        ).translate(text)
    except:
        return text

# --- ANALYZE CROP IMAGE ---
def analyze_crop(image, language_code):
    try:
        model = genai.GenerativeModel("gemini-2.5-flash")

        prompt = """
        You are an expert agricultural scientist.
        Analyze this crop/plant image carefully and provide:

        1. DISEASE NAME: (or "Healthy" if no disease)
        2. CONFIDENCE: (High/Medium/Low)
        3. AFFECTED PART: (Leaf/Stem/Root/Fruit)
        4. SYMPTOMS: (What you can see)
        5. CAUSES: (Why this disease occurs)
        6. TREATMENT: (Step by step treatment)
        7. MEDICINE: (Specific medicine/pesticide names)
        8. PREVENTION: (How to prevent in future)
        9. SEVERITY: (Mild/Moderate/Severe)
        10. ESTIMATED YIELD LOSS: (percentage if untreated)

        Be specific, practical and helpful for Indian farmers.
        Format each point clearly with the number and label.
        """

        response = model.generate_content([prompt, image])
        result = response.text

        # Translate if needed
        if language_code != "en":
            result = translate_text(result, language_code)

        return result

    except Exception as e:
        return f"❌ Analysis failed: {str(e)}"

# --- TEXT TO SPEECH ---
def speak_result(text, lang_code):
    try:
        # Clean text for speech
        clean_text = text[:500]
        tts = gTTS(text=clean_text, lang=lang_code)
        audio_file = "assets/result_audio.mp3"
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
            🌿 Crop Scanner | 👤 {user['full_name']}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # --- HEADER ---
    st.markdown("""
    <div class="section-header">
        🌿 AI Crop Disease Scanner
    </div>
    """, unsafe_allow_html=True)

    # --- DESCRIPTION ---
    st.markdown("""
    <div style="
        background: #E8F5E9;
        border-radius: 16px;
        padding: 20px;
        margin-bottom: 24px;
        border-left: 5px solid #2E7D32;
    ">
        <div style="
            font-size:16px;
            color:#1B5E20;
            font-weight:600;
        ">
            📸 How to use:
        </div>
        <div style="
            font-size:14px;
            color:#555;
            margin-top:8px;
            line-height:1.8;
        ">
            1️⃣ Upload a clear photo of your crop leaf or plant<br>
            2️⃣ Click "Analyze Crop" button<br>
            3️⃣ Get instant AI diagnosis in your language<br>
            4️⃣ Listen to result with voice output<br>
            5️⃣ Result saved in your scan history
        </div>
    </div>
    """, unsafe_allow_html=True)

    # --- TWO COLUMNS ---
    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown("""
        <div style="
            font-size:16px;
            font-weight:600;
            color:#2E7D32;
            margin-bottom:12px;
        ">
            📤 Upload Crop Image
        </div>
        """, unsafe_allow_html=True)

        # Upload option
        upload_type = st.radio(
            "Choose input method:",
            ["📁 Upload from Gallery",
             "📷 Use Camera"],
            horizontal=True
        )

        image = None

        if upload_type == "📁 Upload from Gallery":
            uploaded = st.file_uploader(
                "Choose crop image",
                type=["jpg", "jpeg", "png", "webp"],
                help="Upload a clear image of the crop"
            )
            if uploaded:
                image = Image.open(uploaded)

        else:
            camera = st.camera_input(
                "Take a photo of your crop"
            )
            if camera:
                image = Image.open(camera)

        # Language selector
        st.markdown("<br>", unsafe_allow_html=True)
        selected_lang = st.selectbox(
            "🌐 Result Language",
            list(LANGUAGES.keys()),
            index=list(LANGUAGES.keys()).index(lang)
        )
        lang_code = LANGUAGES[selected_lang]

    with col2:
        if image:
            st.markdown("""
            <div style="
                font-size:16px;
                font-weight:600;
                color:#2E7D32;
                margin-bottom:12px;
            ">
                🖼️ Your Crop Image
            </div>
            """, unsafe_allow_html=True)

            st.image(
                image,
                caption="Uploaded crop image",
                use_column_width=True
            )
        else:
            st.markdown("""
            <div style="
                background: #F1F8E9;
                border-radius: 16px;
                padding: 60px 20px;
                text-align: center;
                border: 2px dashed #81C784;
            ">
                <div style="font-size:60px;">🌿</div>
                <div style="
                    font-size:16px;
                    color:#888;
                    margin-top:12px;
                ">
                    Upload your crop image here
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # --- ANALYZE BUTTON ---
    if image:
        if st.button(
            "🔬 Analyze Crop Now",
            use_container_width=True
        ):
            with st.spinner(
                "🤖 AI is analyzing your crop..."
            ):
                time.sleep(1)
                result = analyze_crop(image, lang_code)

            # --- SHOW RESULT ---
            st.markdown("""
            <div class="section-header">
                📋 Analysis Result
            </div>
            """, unsafe_allow_html=True)

            st.markdown(f"""
            <div class="result-box">
                <div style="
                    font-size:14px;
                    color:#555;
                    line-height:1.9;
                    white-space:pre-wrap;
                ">
                    {result}
                </div>
            </div>
            """, unsafe_allow_html=True)

            # --- SAVE TO HISTORY ---
            try:
                # Extract disease name from result
                lines = result.split('\n')
                disease = "Unknown"
                for line in lines:
                    if "DISEASE" in line.upper():
                        disease = line.split(":")[-1].strip()
                        break

                save_scan(
                    user_id=user['id'],
                    image_path="uploaded_image",
                    disease_name=disease,
                    confidence="AI Analysis",
                    treatment=result[:500]
                )
                st.success(
                    "✅ Result saved to your scan history!"
                )
            except:
                pass

            # --- VOICE OUTPUT ---
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("""
            <div style="
                font-size:16px;
                font-weight:600;
                color:#FF6F00;
            ">
                🔊 Listen to Result
            </div>
            """, unsafe_allow_html=True)

            if st.button(
                "🔊 Play Voice Result",
                use_container_width=True
            ):
                with st.spinner("Generating audio..."):
                    audio = speak_result(
                        result, lang_code
                    )
                    if audio and os.path.exists(audio):
                        st.audio(audio)
                    else:
                        st.warning(
                            "⚠️ Voice not available "
                            "for this language"
                        )

    # --- TIPS SECTION ---
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div class="section-header">
        💡 Photography Tips for Better Results
    </div>
    """, unsafe_allow_html=True)

    tips_col1, tips_col2 = st.columns(2)

    with tips_col1:
        st.markdown("""
        <div class="card">
            <div class="card-icon">✅</div>
            <div class="card-title">Good Photos</div>
            <div style="
                font-size:14px;
                color:#555;
                line-height:1.8;
                margin-top:8px;
            ">
                ✅ Clear and focused image<br>
                ✅ Good natural lighting<br>
                ✅ Close up of affected area<br>
                ✅ Single leaf or plant part<br>
                ✅ Plain background if possible
            </div>
        </div>
        """, unsafe_allow_html=True)

    with tips_col2:
        st.markdown("""
        <div class="card" style="border-color:#C62828;">
            <div class="card-icon">❌</div>
            <div class="card-title">Avoid These</div>
            <div style="
                font-size:14px;
                color:#555;
                line-height:1.8;
                margin-top:8px;
            ">
                ❌ Blurry or dark photos<br>
                ❌ Too far from plant<br>
                ❌ Multiple plants in frame<br>
                ❌ Night time photos<br>
                ❌ Dirty camera lens
            </div>
        </div>
        """, unsafe_allow_html=True)