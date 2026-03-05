import streamlit as st
import google.generativeai as genai

# --- 1. SETUP ---
st.set_page_config(page_title="Comedy Crowd Sim", page_icon="🎤", layout="wide")

# This will now pull from your NEW API key in the NEW project
api_key = st.secrets.get("api_key")
if not api_key:
    st.error("Missing API Key in Streamlit Secrets!")
    st.stop()

# Force the stable production configuration
genai.configure(api_key=api_key, transport='rest')

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

# --- 4. MAIN INTERFACE ---
st.title("🎤 Comedy Crowd Sim")
st.markdown(f"**Current Stage:** Live from {city}")

bit_text = st.text_area("Paste your set here:", height=300, placeholder="The AI will simulate the room and tell you if it actually lands...")

if st.button("🚀 Run Simulation", use_container_width=True):
    if bit_text and sel_crowds and sel_ages and sel_vibes:
        
        # Use the most stable Tier 1 model name
        model_name = 'gemini-1.5-flash' 
        
        try:
            model = genai.GenerativeModel(model_name)
            
            prompt = f"""
            You are a Professional Comedy Simulation Engine.
            VENUE: {city} | AUDIENCE: {', '.join(sel_crowds)} | AGES: {', '.join(sel_ages)} | VIBE: {', '.join(sel_vibes)}
            
            BIT:
            {bit_text}
            
            RESPONSE STRUCTURE:
            1. THE ROOM SOUND: (Literal background noise, laughter levels, or awkward silence)
            2. AUDIENCE PERSONAS: (3 distinct reactions—who laughed, who stared, and who checked their phone?)
            3. IS IT FUNNY?: (A blunt assessment of the humor based on the generational and venue context.)
            4. SCORECARD: Laughter %, Tension %, Kill Probability %
            5. THE TAG: (Suggest one short, sharp 'tag' to save or boost the bit.)
            """
            
            with st.spinner(f'Checking the room via {model_name}...'):
                # Safety settings set to BLOCK_NONE so edgy content isn't censored
                response = model.generate_content(
                    prompt,
                    safety_settings=[
                        {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
                        {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"}
                    ]
                )
                st.markdown("---")
                st.markdown(response.text)
                if "100%" in response.text: st.balloons()
                
        except Exception as e:
            st.error(f"Handshake Error: {e}")
            st.info("If you just enabled billing, it may take 10-30 minutes for the API key to activate.")
    else:
        st.warning("Please check at least one box in every category (Audience, Age, and Vibe)!")
