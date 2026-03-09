import streamlit as st
import pandas as pd
from google import genai
from google.genai import types

# 1. PAGE SETUP
st.set_page_config(page_title="Comedy Crowd Sim", page_icon="🎤", layout="wide")

# 2. CSS (Navy & Yellow - "Deep Dive" Theme)
st.markdown("""
<style>
    .main { background-color: #f8fbff; }
    .main-title { color: #1e3a8a; font-weight: 800; text-align: center; border: 3px solid #1e3a8a; padding: 20px; border-radius: 20px; background-color: #ffffff; margin-bottom: 30px; }
    .stButton button { background-color: #facc15 !important; color: #1e3a8a !important; border: 2px solid #1e3a8a !important; font-weight: bold !important; border-radius: 12px !important; width: 100%; height: 3em; }
    [data-testid="stSidebar"] { background-color: #1e3a8a !important; color: white !important; }
    .crowd-response { background-color: #eff6ff; border-left: 10px solid #facc15; padding: 25px; border-radius: 15px; color: #1e3a8a; margin-top: 20px; white-space: pre-wrap; font-size: 1.1em; }
    .tooltip-box { background-color: #fef08a; padding: 10px; border-radius: 8px; font-size: 0.9em; color: #1e3a8a; border: 1px solid #facc15; margin-bottom: 10px; }
</style>
""", unsafe_allow_html=True)

# 3. API SETUP
try:
    api_key = st.secrets["api_key"]
    client = genai.Client(api_key=api_key)
except Exception:
    st.error("🔑 API Key Missing!")
    st.stop()

# 4. SIDEBAR - THE "SHOW RUNNER" SETTINGS
with st.sidebar:
    st.header("🏫 CLASSROOM/VENUE SETUP")
    
    city = st.text_input("City", value="San Luis Obispo", help="Where the show is taking place.")
    venue_type = st.selectbox("Venue Type", ["Dive Bar", "Theater", "Casino", "Outdoor Festival", "Wine Cellar"])
    
    st.markdown("---")
    
    st.subheader("👥 Audience Makeup")
    crowd_vibe = st.selectbox("Crowd Vibe", ["Supportive", "Indifferent", "Hostile", "Rowdy", "Intellectual"])
    age_range = st.select_slider("Main Age Group", options=["Gen Z", "Millennials", "Gen X", "Boomers"], value="Millennials")
    
    st.markdown("---")
    
    # THE "DEEP DIVE" TOOLTIP FEATURES
    st.subheader("🛠️ SIMULATOR MODES")
    lk = st.checkbox("Lock Structure", help="Keep the AI from rewriting your setup; focus only on the punchline.")
    coach_mode = st.checkbox("Coach Mode", help="Get a 'Professor' style critique along with the crowd reaction.")
    local_refs = st.checkbox("Local Refs", help="Force the AI to mention local SLO landmarks or culture.")

# 5. MAIN UI
st.markdown("<h1 class='main-title'>🎤 COMEDY CROWD SIMULATOR</h1>", unsafe_allow_html=True)

# Placeholder Instructions
st.markdown("""
<div class="tooltip-box">
    <strong>💡 Pro-Tip:</strong> Use 'Coach Mode' if you're prepping for a TPA-style pedagogical reflection on your set.
</div>
""", unsafe_allow_html=True)

joke_input = st.text_area("Your Bit / Lesson Opener:", height=300, placeholder="Paste your bit here...")

# 6. RUN THE SIMULATION
if st.button("🚀 DELIVER TO CROWD"):
    if not joke_input:
        st.warning("The mic is live, but you're not speaking! Paste a bit.")
    else:
        with st.spinner("The room is sizing you up
