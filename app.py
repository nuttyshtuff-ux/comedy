import streamlit as st
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold

# --- 1. SETUP ---
st.set_page_config(page_title="Comedy Crowd Sim", page_icon="🎤", layout="wide")

api_key = st.secrets.get("api_key")
if not api_key:
    st.error("Missing API Key in Secrets!")
    st.stop()

# Force the configuration to use the stable v1 API
genai.configure(api_key=api_key)

# --- 2. DATA ---
CROWDS = ["Underground Comedy", "The Comedy Shop", "Don't Tell", "The College Gig", "Dive Bar", "Upscale Bar", "Comedy Showcase", "Open Mic Night"]
AGES = ["Gen Z", "Millennials", "Gen X", "Boomers"]
VIBES = ["Normal", "Hostile/Heckling", "Distracted", "Drunk", "Passive", "New to Comedy", "Skeptical but Hopeful", "Jaded", "Friendly", "Silence for No Reason", "Easily Offended", "Chatty", "Other Comics Watching"]

# --- 3. SIDEBAR ---
with st.sidebar:
    st.title("🎤 Room Setup")
    city = st.text_input("City", value="San Luis Obispo")
    
    st.markdown("---")
    st.header("1. The Audience")
    sel_crowds = [c for c in CROWDS if st.checkbox(c, key=f"c_{c}")]
    
    st.header("2. Age Range")
    sel_ages = [a for a in AGES if st.checkbox(a, key=f"a_{a}")]
    
    st.header("3. The Vibe")
    sel_vibes = [v for v in VIBES if st.checkbox(v, key=f"v_{v}")]

# --- 4. MAIN ---
st.title("🎤 Comedy Crowd Sim")
bit_text = st.text_area("Paste your set here:", height=300)

if st.button("🚀 Run Simulation", use_container_width=True):
    if bit_text and sel_crowds and sel_ages and sel_vibes:
        
        # We use the versionless 'gemini-1.5-flash' - this is the "stable" path
        # If Flash fails, we try 'gemini-1.5-pro'
        success = False
        last_error = ""
        
        for m_name in ['gemini-1.5-flash', 'gemini-1.5-pro']:
            if success: break
            try:
                # Use the stable model constructor
                model = genai.GenerativeModel(m_name)
                
                prompt = f"""
                You are a Professional Comedy Simulation Engine.
                VENUE: {city} | AUDIENCE: {', '.join(sel_crowds)} | AGES: {', '.join(sel_ages)} | VIBE: {', '.join(sel_vibes)}
                BIT: {bit_text}
                
                RESPONSE:
                1. THE ROOM SOUND
                2. AUDIENCE PERSONAS
                3. IS IT FUNNY? (Blunt assessment)
                4. SCORECARD (Laughter %, Tension %, Kill Probability %)
                5. THE TAG
                """
                
                with st.spinner(f'Live from the {m_name} server...'):
                    # Setting safety to BLOCK_NONE so it doesn't flag your 'vibrator' line
                    response = model.generate_content(
                        prompt,
                        safety_settings={
                            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
                            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                        }
                    )
                    st.markdown("---")
                    st.markdown(response.text)
                    success = True
            except Exception as e:
                last_error = str(e)
                continue
        
        if not success:
            st.error(f"Handshake Error: {last_error}")
            st.info("Check Google AI Studio: Is the 'Generative Language API' enabled for your project?")
    else:
        st.warning("Please check at least one box in every category!")
