import streamlit as st
import google.generativeai as genai

# --- 1. SETUP & AUTH ---
st.set_page_config(page_title="Comedy Crowd Sim", page_icon="🎤", layout="wide")

# Retrieve the key from Secrets
api_key = st.secrets.get("api_key")
if not api_key:
    st.error("API Key not found! Go to Streamlit -> Settings -> Secrets and add: api_key = 'YOUR_KEY'")
    st.stop()

# Configure the SDK
genai.configure(api_key=api_key)

# --- 2. DATA CONSTANTS ---
CROWDS = ["Underground Comedy", "The Comedy Shop", "Don't Tell", "College Gig", "Biker Bar", "VFW Hall", "Tech Mixer", "Open Mic Night", "The Woke Workshop"]
VIBES = ["Normal", "Hostile/Heckling", "Distracted", "Drunk 20-Somethings", "Passive", "New to Comedy", "Skeptical", "Jaded", "Friendly"]
STYLES = ["Observational", "Deadpan/One-Liners", "Storytelling", "Self-Deprecating", "High Energy/Physical", "Political", "Absurdist"]

# --- 3. SIDEBAR UI ---
with st.sidebar:
    st.title("🎤 Room Setup")
    city = st.text_input("City/Venue", value="San Luis Obispo")
    
    st.header("1. The Audience")
    sel_crowds = [c for c in CROWDS if st.checkbox(c, key=f"c_{c}")]
    
    st.header("2. The Vibe")
    sel_vibes = [v for v in VIBES if st.checkbox(v, key=f"v_{v}")]
    
    st.header("3. Performance Style")
    sel_styles = [s for s in STYLES if st.checkbox(s, key=f"s_{s}")]

# --- 4. MAIN INTERFACE ---
st.title("🎤 Comedy Crowd Sim")
st.markdown(f"**Current Stage:** Live from {city}")

bit_text = st.text_area("Paste your set here:", height=300, placeholder="Paste your bit here...")

if st.button("🚀 Run Simulation", use_container_width=True):
    if bit_text and sel_crowds and sel_vibes and sel_styles:
        
        # 2026 STABLE MODELS FOR TIER 1 ACCOUNTS
        # We start with 2.0-flash as it is the fastest and most likely to be active
        models_to_try = ['gemini-2.0-flash', 'gemini-1.5-pro', 'gemini-1.5-flash']
        
        # Safety settings (BLOCK_NONE allows for edgy comedy content)
        safety = [
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
        ]
        
        success = False
        last_error = ""
        
        for m_name in models_to_try:
            if success: break
            try:
                # Use the GenerativeModel class with the current name
                model = genai.GenerativeModel(model_name=m_name, safety_settings=safety)
                
                prompt = f"""
                You are a Professional Comedy Simulation Engine. 
                VENUE: {city}
                AUDIENCE TYPE: {', '.join(sel_crowds)}
                CURRENT MOOD: {', '.join(sel_vibes)}
                COMIC STYLE: {', '.join(sel_styles)}
                
                THE BIT:
                {bit_text}
                
                OUTPUT:
                1. THE ROOM SOUND: (Describe the auditory vibe)
                2. AUDIENCE PERSONAS: (3 distinct reactions from locals)
