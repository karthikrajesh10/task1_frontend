import streamlit as st
import requests
from st_audiorec import st_audiorec

API_BASE = "http://127.0.0.1:8000"

st.set_page_config(page_title="Voice Assistant", layout="centered")
st.title("🗣️ Voice Assistant")

# ---------------- SESSION STATE ----------------

if "token" not in st.session_state:
    st.session_state.token = None

if "page" not in st.session_state:
    st.session_state.page = "login"

# ---------------- AUTH ----------------

def signup():
    st.subheader("Signup")
    u = st.text_input("Username")
    p = st.text_input("Password", type="password")

    if st.button("Create account"):
        r = requests.post(
            f"{API_BASE}/auth/signup",
            json={"username": u, "password": p}
        )
        if r.status_code == 200:
            st.success("Signup successful. Please login.")
            st.session_state.page = "login"
            st.rerun()
        else:
            st.error(r.text)


def login():
    st.subheader("Login")
    u = st.text_input("Username")
    p = st.text_input("Password", type="password")

    if st.button("Login"):
        r = requests.post(
            f"{API_BASE}/auth/login",
            json={"username": u, "password": p}
        )
        if r.status_code == 200:
            st.session_state.token = r.json()["access_token"]
            st.session_state.page = "chat"
            st.rerun()
        else:
            st.error("Invalid credentials")


if st.session_state.page == "signup":
    signup()
    if st.button("Already have an account? Login"):
        st.session_state.page = "login"
        st.rerun()

elif st.session_state.page == "login":
    login()
    if st.button("New user? Signup"):
        st.session_state.page = "signup"
        st.rerun()

# ---------------- CHAT ----------------

elif st.session_state.page == "chat":

    with st.sidebar:
        st.markdown("### Settings")

        language = st.selectbox(
            "Voice language",
            ["en", "ml", "hi", "ta"],
            index=0
        )

        if st.button("🚪 Logout"):
            st.session_state.clear()
            st.rerun()

    st.markdown("---")

    # -------- TEXT INPUT --------
    st.subheader("💬 Text input")

    text = st.text_input("Type a message")

    if st.button("Send text") and text.strip():
        r = requests.post(
            f"{API_BASE}/chat",
            headers={"Authorization": f"Bearer {st.session_state.token}"},
            data={"text": text, "language": language}
        )

        if r.status_code == 200:
            res = r.json()
            st.markdown(f"**English:** {res['english_text']}")
            st.audio(API_BASE + res["audio"])
        else:
            st.error(r.text)

    st.markdown("---")

    # -------- VOICE INPUT --------
    st.subheader("🎙️ Voice input")

    wav_audio_data = st_audiorec()

    if wav_audio_data is not None:
        st.success("Voice recorded")

        files = {
            "audio": ("voice.wav", wav_audio_data, "audio/wav")
        }

        data = {"language": language}

        r = requests.post(
            f"{API_BASE}/chat",
            headers={"Authorization": f"Bearer {st.session_state.token}"},
            files=files,
            data=data
        )

        if r.status_code == 200:
            res = r.json()
            st.markdown(f"**Original:** {res.get('original_text')}")
            st.markdown(f"**English:** {res['english_text']}")
            st.audio(API_BASE + res["audio"])
        else:
            st.error(r.text)
