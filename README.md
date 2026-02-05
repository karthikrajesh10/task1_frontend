VOICE ASSISTANT FRONTEND (STREAMLIT UI)

This Streamlit application is the frontend for the Voice Assistant
system.

It connects to the FastAPI backend and allows users to:

-   Signup and Login
-   Chat using text
-   Chat using voice input
-   Listen to audio responses from the assistant

------------------------------------------------------------------------

HOW IT WORKS

User (Browser) | v Streamlit Frontend | | HTTP Requests (JSON /
Multipart) v FastAPI Backend (Auth + STT + RAG + TTS)

The frontend sends requests to the backend and displays: - Text
responses - Translated text (for voice input) - Audio responses

------------------------------------------------------------------------

INSTALLATION

Make sure Python is installed.

Install the required dependencies:

pip install streamlit requests st-audiorec

------------------------------------------------------------------------

RUN THE APPLICATION

From the folder where app.py is located, run:

streamlit run app.py

Streamlit will open automatically in your browser at:
http://localhost:8501

------------------------------------------------------------------------

STEP 1 — SIGNUP

1.  Open the app
2.  Go to Signup section
3.  Enter Username and Password
4.  Click Create Account

This creates a user in the backend.

------------------------------------------------------------------------

STEP 2 — LOGIN

1.  Go to Login section
2.  Enter your credentials
3.  On success, the app stores the JWT token
4.  You are now authenticated to use the chat

------------------------------------------------------------------------

STEP 3 — TEXT CHAT

-   Enter your question in the text box
-   Select language (example: en)
-   Submit

You will receive: - Answer text - Audio response

------------------------------------------------------------------------

STEP 4 — VOICE CHAT

-   Record your voice using the recorder
-   Select the language you spoke (ml / hi / en)
-   Submit

The app will: 1. Convert voice to text (STT) 2. Retrieve answer using
RAG 3. Convert answer to audio (TTS)

You will see: - Original spoken text - English translation - Audio
response

------------------------------------------------------------------------

BACKEND REQUIREMENT

Make sure the FastAPI backend is running before starting Streamlit.

Backend URL: http://127.0.0.1:8000

Swagger docs: http://127.0.0.1:8000/docs

------------------------------------------------------------------------

FEATURES

-   Text and Voice interaction
-   JWT-based authenticated requests
-   Audio playback inside the UI
-   Multi-language voice support
-   Simple and clean interface

------------------------------------------------------------------------

SUMMARY

-   Streamlit UI
-   Works with FastAPI backend
-   Supports Signup, Login, Text Chat, Voice Chat
-   Displays both text and audio responses
