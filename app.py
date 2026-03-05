import streamlit as st
from google import genai
from google.genai import types

# --- 1. SETUP ---
st.set_page_config(page_title="Comedy Crowd Sim", page_icon="🎤", layout="wide")

# Ensure your Streamlit Secret is named 'api_key'
api_key = st.secrets.get("api_key")
if not api_key:
    st.error("Missing API Key in Streamlit Secrets!")
    st.stop()

# INITIALIZE CLIENT: Force the v1 production endpoint
# This is the fix for the v1beta 404 error.
try:
    client = genai.Client(
        api_key=api_key,
        http_options={'api_version': 'v1'}
    )
except Exception as e:
    st.error(f"Initialization Error: {e}")
    st.stop()

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

    # COACH MODE AT BOTTOM
    st.markdown("---")
    st.header("💡 Pro Mode")
    coach_mode = st.checkbox("Coach Me on This Room", value=False, help="Get psychological advice for this specific crowd.")

# --- 4. MAIN INTERFACE ---
st.title("🎤 Comedy Crowd Sim")
bit_text = st.text_area("Paste your set here:", height=300, placeholder="Wait for the rebuild, then paste your bit...")

if st.button("🚀 Run Simulation", use_container_width=True):
    if bit_text and sel_crowds and sel_ages and sel_vibes:
        try:
            # Constructing the instruction for the AI
            coach_instruction = ""
            if coach_mode:
                coach_instruction = f"""
                COACH'S CORNER: Before the simulation, provide a section called 'COACH'S CORNER'. 
                Give specific advice on how to handle {', '.join(sel_ages)} in a {', '.join(sel_crowds)} venue with a {', '.join(sel_vibes)} vibe.
                """

            prompt = f"""
            SYSTEM: You are a Professional Comedy Simulation Engine.
            {coach_instruction}
            
            VENUE: {', '.join(sel_crowds)} | AGES: {', '.join(sel_ages)} | VIBE: {', '.join(sel_vibes)} | CITY: {city}
            BIT: {bit_text}
            
            STRUCTURE:
            (Start with COACH'S CORNER if active)
            1. THE ROOM SOUND (Literal background noise and laughter)
            2. AUDIENCE PERSONAS (3 distinct person reactions)
            3. IS IT FUNNY? (Blunt, honest feedback)
            4. SCORECARD (Laughter %, Tension %, Kill Probability %)
            5. THE TAG (One sharp line to add to the bit)
            """
            
            with st.spinner('Accessing the V1 Production API...'):
                # THE NEW SDK SYNTAX
                response = client.models.generate_content(
                    model="gemini-1.5-flash",
                    contents=prompt
                )
                
                st.markdown("---")
                st.markdown(response.text)
                if "100%" in response.text: st.balloons()
                
        except Exception as e:
            st.error(f"API Error: {e}")
            if "404" in str(e):
                st.warning("Still seeing 404? This is a 'Stale API Key' issue. Create a NEW Key in a NEW Project in AI Studio.")
    else:
        st.warning("Please check at least one box in every category!")
