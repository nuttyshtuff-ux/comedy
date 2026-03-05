import streamlit as st
import google.generativeai as genai

# --- 1. SETUP ---
st.set_page_config(page_title="Comedy Crowd Sim", page_icon="🎤", layout="wide")

api_key = st.secrets.get("api_key")
if not api_key:
    st.error("Missing API Key in Streamlit Secrets!")
    st.stop()

# THE FIX: Explicitly tell the library to use 'v1' (not v1beta)
# This is the "Stable" lane for Paid Tier accounts
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

    st.markdown("---")
    st.header("💡 Pro Mode")
    coach_mode = st.checkbox("Coach Me on This Room", value=False)

# --- 4. MAIN ---
st.title("🎤 Comedy Crowd Sim")
bit_text = st.text_area("Paste your set here:", height=300)

if st.button("🚀 Run Simulation", use_container_width=True):
    if bit_text and sel_crowds and sel_ages and sel_vibes:
        
        try:
            # We are calling the model without 'v1beta' in the path
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            coach_instruction = ""
            if coach_mode:
                coach_instruction = f"Provide a 'COACH'S CORNER' with advice for {sel_ages} in {sel_crowds}."

            prompt = f"ACT AS A COMEDY AUDIENCE. {coach_instruction} VENUE: {sel_crowds} | VIBE: {sel_vibes} | BIT: {bit_text}"
            
            with st.spinner('Accessing the V1 Stable Server...'):
                # This call will now target /v1/ instead of /v1beta/
                response = model.generate_content(prompt)
                
                st.markdown("---")
                st.markdown(response.text)
                if "100%" in response.text: st.balloons()
                
        except Exception as e:
            st.error(f"Error: {e}")
            st.info("Check Google AI Studio: Is 'Generative Language API' enabled for your project?")
    else:
        st.warning("Please check at least one box in every category!")
