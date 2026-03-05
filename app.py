import streamlit as st
import google.generativeai as genai

# --- 1. SETUP ---
st.set_page_config(page_title="Comedy Crowd Sim", page_icon="🎤", layout="wide")

api_key = st.secrets.get("api_key")
if not api_key:
    st.error("Missing API Key in Secrets!")
    st.stop()

genai.configure(api_key=api_key)

# --- 2. DATA ---
CROWDS = ["Underground Comedy", "The Comedy Shop", "Don't Tell", "The College Gig", "Dive Bar", "Upscale Bar", "Comedy Showcase", "Open Mic Night"]
AGES = ["Gen Z", "Millennials", "Gen X", "Boomers"]
VIBES = ["Normal", "Hostile/Heckling", "Distracted", "Drunk", "Passive", "New to Comedy", "Skeptical but Hopeful", "Jaded", "Friendly", "Silence for No Reason", "Easily Offended", "Chatty", "Other Comics Watching"]

# --- 3. SIDEBAR ---
with st.sidebar:
    st.title("🎤 Room Setup")
    city = st.text_input("City", value="San Luis Obispo")
    sel_crowds = [c for c in CROWDS if st.checkbox(c, key=f"c_{c}")]
    sel_ages = [a for a in AGES if st.checkbox(a, key=f"a_{a}")]
    sel_vibes = [v for v in VIBES if st.checkbox(v, key=f"v_{v}")]

# --- 4. MAIN ---
st.title("🎤 Comedy Crowd Sim")
bit_text = st.text_area("Paste your set here:", height=300)

if st.button("🚀 Run Simulation", use_container_width=True):
    if bit_text and sel_crowds and sel_ages and sel_vibes:
        
        # TRIAGE: Try the most stable production models
        # Using 1.5-pro as the primary for Paid Tier stability
        models_to_try = ['gemini-1.5-pro', 'gemini-1.5-flash', 'gemini-pro']
        
        success = False
        last_error = ""
        
        for m_name in models_to_try:
            if success: break
            try:
                model = genai.GenerativeModel(model_name=m_name)
                prompt = f"""
                Analyze this comedy bit for a {city} crowd.
                AUDIENCE: {', '.join(sel_crowds)} | AGES: {', '.join(sel_ages)} | VIBE: {', '.join(sel_vibes)}
                
                BIT:
                {bit_text}
                
                OUTPUT:
                1. THE ROOM SOUND
                2. AUDIENCE PERSONAS
                3. IS IT FUNNY? (Blunt assessment)
                4. SCORECARD (Laughter %, Tension %, Kill Probability %)
                5. THE TAG
                """
                
                with st.spinner(f'Consulting {m_name}...'):
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
                    success = True
            except Exception as e:
                last_error = str(e)
                continue
        
        if not success:
            st.error(f"Handshake Error: {last_error}")
            st.info("Check Google AI Studio to ensure your 'Paid' status is fully active.")
    else:
        st.warning("Check at least one box in every sidebar category!")
