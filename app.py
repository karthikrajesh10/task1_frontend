import streamlit as st
import os
import speech_recognition as sr
from datetime import datetime

from tts_stt_backend.backend.chat_service import process_chat
from tts_stt_backend.backend.stt_service import speech_to_text


# ---------------- Page Config ----------------
st.set_page_config(
    page_title="Voice Assistant Chatbot",
    page_icon="🗣️",
    layout="centered"
)

st.title("🗣️ Voice Assistant Chatbot")
st.caption("STT & TTS with Multilanguage Support")

OUTPUT_DIR = "output/audio"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ---------------- Session State ----------------
if "chats" not in st.session_state:
    st.session_state.chats = {1: []}

if "current_chat_id" not in st.session_state:
    st.session_state.current_chat_id = 1

# ---------------- Sidebar ----------------
with st.sidebar:
    st.header("💬 Chats")

    if st.button("➕ New Chat"):
        new_id = max(st.session_state.chats.keys()) + 1
        st.session_state.chats[new_id] = []
        st.session_state.current_chat_id = new_id
        st.rerun()

    st.divider()

    for cid in st.session_state.chats:
        if st.button(f"Chat {cid}", key=f"chat_{cid}"):
            st.session_state.current_chat_id = cid
            st.rerun()

    st.divider()

    # -------- Language Selection --------
    st.header("🌍 Speech Language")

    language_option = st.selectbox(
        "Select language",
        ["Auto Detect", "English", "Hindi", "Tamil", "Malayalam", "Telugu"]
    )

    LANGUAGE_MAP = {
        "English": "en",
        "Hindi": "hi",
        "Tamil": "ta",
        "Malayalam": "ml",
        "Telugu": "te"
    }

    selected_language = None if language_option == "Auto Detect" else LANGUAGE_MAP[language_option]

    st.divider()
    st.header("🎤 Voice Input")

    if st.button("🎙️ Start Voice Input"):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            st.info("Listening...")
            audio = r.listen(source)

        audio_path = os.path.join(OUTPUT_DIR, "voice_input.wav")
        with open(audio_path, "wb") as f:
            f.write(audio.get_wav_data())

        # Engine-independent STT call with language
        st.session_state.voice_input = speech_to_text(audio_path, selected_language)
        st.success("Voice converted to text")

# ---------------- Display Chat ----------------
messages = st.session_state.chats[st.session_state.current_chat_id]

for msg in messages:
    with st.chat_message(msg["role"]):
        if "original_text" in msg:
            st.markdown(f"**🗣️ You said (Original):** {msg['original_text']}")
            st.markdown(f"**🌍 English Translation:** {msg['content']}")
        else:
            st.write(msg["content"])

        if "audio" in msg:
            st.audio(msg["audio"])
        st.caption(msg["time"])

# ---------------- Input ----------------
user_input = st.chat_input("Type your message...")

# If voice input exists, treat it as user input
if "voice_input" in st.session_state:
    user_input = st.session_state.voice_input
    del st.session_state.voice_input

if user_input:
    time_now = datetime.now().strftime("%H:%M")

    messages.append({
        "role": "user",
        "content": user_input,
        "time": time_now
    })

    assistant_msg = process_chat(
        user_input,
        st.session_state.current_chat_id,
        len(messages)
    )

    messages.append(assistant_msg)
    st.rerun()
