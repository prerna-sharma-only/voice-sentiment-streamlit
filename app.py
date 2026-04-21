import streamlit as st
from transformers import pipeline
import speech_recognition as sr
import tempfile
import time

st.set_page_config(page_title="Voice Sentiment AI", layout="centered")



# 🌈 PREMIUM CSS (UPDATED WAVE)
st.markdown("""
<style>

/* 🌌 GLOBAL BACKGROUND */
body {
    background: radial-gradient(circle at center, #020d0d, #000000);
    color: #00ffcc;
    overflow-x: hidden;
}

/* 🧠 MAIN HUD FRAME FIXED */
.block-container {
    max-width: 900px;
    margin: auto;
    position: relative;
}

/* BORDER */
.block-container::before {
    content: "";
    position: absolute;
    top: -20px;
    left: -20px;
    right: -20px;
    bottom: -20px;
    border: 2px solid rgba(0,255,200,0.2);
    border-radius: 20px;
    pointer-events: none;
    box-shadow: 
        0 0 20px rgba(0,255,200,0.2),
        inset 0 0 20px rgba(0,255,200,0.1);
}

/* SCANNING LINE */
.block-container::after {
    content: "";
    position: absolute;
    top: -20px;
    left: -20px;
    right: -20px;
    bottom: -20px;
    border-radius: 20px;
    pointer-events: none;
    background: linear-gradient(90deg, transparent, #00ffcc, transparent);
    background-size: 200% 2px;
    background-repeat: no-repeat;
    animation: scanline 3s linear infinite;
}

@keyframes scanline {
    0% { background-position: -200% 0; }
    100% { background-position: 200% 0; }
}

/* 🧩 GRID OVERLAY */
body::before {
    content: "";
    position: fixed;
    width: 100%;
    height: 100%;
    background-image: 
        linear-gradient(rgba(0,255,200,0.05) 1px, transparent 1px),
        linear-gradient(90deg, rgba(0,255,200,0.05) 1px, transparent 1px);
    background-size: 40px 40px;
    pointer-events: none;
}

/* ✨ TITLE */
.title {
    font-size: 50px;
    font-weight: bold;
    color: #00ffcc;
    text-shadow: 0 0 20px #00ffcc;
}

/* SUBTITLE */
.subtitle {
    color: #00ffaa;
    opacity: 0.7;
}


/* INPUT FIXED (target only real input) */
.stTextInput input {
    background: rgba(0,255,200,0.05) !important;
    border: 1px solid rgba(0,255,200,0.3) !important;
    color: #00ffcc !important;
    border-radius: 12px !important;
}
.stTextInput input:focus {
    box-shadow: 0 0 20px #00ffcc;
    border: 1px solid #00ffcc !important;
}

/* EMOTION TEXT */
.emotion {
    font-size: 28px;
    color: #00ffcc;
    text-shadow: 0 0 10px #00ffcc;
}

/* 🎧 FUTURISTIC WAVE */
.wave {
    display: flex;
    justify-content: center;
    align-items: flex-end;
    gap: 6px;
    height: 50px;
    margin-top: 20px;
}

.bar {
    width: 6px;
    height: 10px;
    background: #00ffcc;
    border-radius: 10px;
    animation: wave 1s infinite ease-in-out;
    box-shadow: 0 0 15px #00ffcc;
}

.bar:nth-child(2){animation-delay:0.1s;}
.bar:nth-child(3){animation-delay:0.2s;}
.bar:nth-child(4){animation-delay:0.3s;}
.bar:nth-child(5){animation-delay:0.4s;}

@keyframes wave {
    0%,100% {height: 10px;}
    50% {height: 45px;}
}

/* 🔥 GLOW BUTTONS */
button {
    background: transparent !important;
    border: 1px solid #00ffcc !important;
    color: #00ffcc !important;
    box-shadow: 0 0 10px #00ffcc;
}

button:hover {
    background: #00ffcc !important;
    color: black !important;
}

/* 📊 CHART FIX */
canvas {
    filter: drop-shadow(0 0 10px #00ffcc);
}
/* 🔐 AUTH CARD */
.auth-card {
    max-width: 420px;
    margin: auto;
    padding: 40px;
    border-radius: 20px;
    background: rgba(0,255,200,0.05);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(0,255,200,0.2);
    box-shadow: 
        0 0 30px rgba(0,255,200,0.15),
        inset 0 0 20px rgba(0,255,200,0.05);
    text-align: center;
    margin-top: 40px;
}

/* 🔐 AUTH TITLE */
.auth-title {
    font-size: 28px;
    color: #00ffcc;
    margin-bottom: 20px;
    text-shadow: 0 0 10px #00ffcc;
}

/* INPUT FIELD */
.auth-card input {
    background: rgba(0,255,200,0.05) !important;
    border: 1px solid rgba(0,255,200,0.3) !important;
    color: #00ffcc !important;
    border-radius: 10px !important;
}

/* BUTTON */
.auth-btn {
    margin-top: 15px;
}
button[kind="secondary"] {
    border: 1px solid #00ffcc !important;
    color: #00ffcc !important;
    box-shadow: 0 0 10px #00ffcc;
}

button[kind="secondary"]:hover {
    background: #00ffcc !important;
    color: black !important;
}
.stTextInput label {
    display: none;
}

</style>
""", unsafe_allow_html=True)


if "user" not in st.session_state:
    st.session_state.user = None

if "users" not in st.session_state:
    st.session_state.users = {"admin": "1234"}


# ---------------- AUTH SYSTEM ----------------
if not st.session_state.user:

    # 🔥 HERO SECTION
    st.markdown("""
        <div style='text-align:center; padding:40px 20px; margin-bottom:10px;'>

        <h1 style='
            font-size:42px;
            font-weight:700;
            color:#00ffcc;
            text-shadow:0 0 15px #00ffcc, 0 0 40px #00ffcc;
            margin-bottom:10px;
        '>
            Welcome to Voice Sentiment AI
        </h1>

        <p style='
            color:#00ffaa;
            opacity:0.7;
            font-size:16px;
        '>
            Analyze emotions from voice & text in real-time
        </p>

        </div>
    """, unsafe_allow_html=True)

    #  THEN your auth card
    
    st.markdown('<div class="auth-card">', unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["🔐 Login", "🆕 Register"])

    with tab1:
        st.markdown('<div class="auth-title">Access System</div>', unsafe_allow_html=True)

        username = st.text_input("Username", key="login_user")
        password = st.text_input("Password", type="password", key="login_pass")

        if st.button("Login", key="login_btn"):
            if username in st.session_state.users and st.session_state.users[username] == password:
                st.session_state.user = username
                st.success("Access Granted")
                st.rerun()
            else:
                st.error("Access Denied")

    with tab2:
        st.markdown('<div class="auth-title">Create Account</div>', unsafe_allow_html=True)

        new_user = st.text_input("New Username", key="reg_user")
        new_pass = st.text_input("New Password", type="password", key="reg_pass")

        if st.button("Register", key="reg_btn"):
            if new_user in st.session_state.users:
                st.warning("User already exists")
            else:
                st.session_state.users[new_user] = new_pass
                st.success("Account Created")

    st.markdown('</div>', unsafe_allow_html=True)

    # ⛔ VERY IMPORTANT
    st.stop()

# logout sidebar
st.sidebar.write(f"👤 {st.session_state.user}")
if st.sidebar.button("Logout"):
    st.session_state.user = None
    st.rerun()





# 🧠 TITLE
st.markdown('<div class="title">🎧 Voice Sentiment AI</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Feel your voice. Understand your emotions.</div>', unsafe_allow_html=True)
st.markdown(f"<div style='color:#00ffcc; opacity:0.7;'>👤 {st.session_state.user}</div>", unsafe_allow_html=True)

# Load model
@st.cache_resource
def load_model():
    return pipeline(
        "text-classification",
        model="j-hartmann/emotion-english-distilroberta-base",
        top_k=None
    )

classifier = load_model()

# ---------------- TEXT INPUT ----------------
text_input = st.text_input("", placeholder="✨ Speak your mind...")

if text_input:
    with st.spinner("Analyzing emotions..."):
        time.sleep(1.2)
        result = classifier(text_input)[0]
        emotions = {i['label']: round(i['score']*100,2) for i in result}
        main = max(emotions, key=emotions.get)

    st.markdown(f'<div class="emotion">Emotion: {main.upper()}</div>', unsafe_allow_html=True)
    st.bar_chart(emotions)

# ---------------- AUDIO ----------------
st.markdown("### 🎧 Upload WAV Audio")
uploaded_file = st.file_uploader("", type=["wav"])

def audio_to_text(file):
    r = sr.Recognizer()
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp:
        temp.write(file.read())
        path = temp.name

    with sr.AudioFile(path) as source:
        audio = r.record(source)

    try:
        return r.recognize_google(audio)
    except:
        return None

if uploaded_file:
    st.audio(uploaded_file)

    with st.spinner("Transcribing audio..."):
        time.sleep(1)
        text = audio_to_text(uploaded_file)

    if text:
        st.info(f"📝 {text}")

        with st.spinner("Analyzing emotions..."):
            st.markdown("""
            <div class="wave">
              <div class="bar"></div>
              <div class="bar"></div>
              <div class="bar"></div>
              <div class="bar"></div>
              <div class="bar"></div>
            </div>
            """, unsafe_allow_html=True)

            time.sleep(1)

            result = classifier(text)[0]
            emotions = {i['label']: round(i['score']*100,2) for i in result}
            main = max(emotions, key=emotions.get)

        st.markdown(f'<div class="emotion">Emotion: {main.upper()}</div>', unsafe_allow_html=True)
        st.bar_chart(emotions)

    else:
        st.error("Could not understand audio")