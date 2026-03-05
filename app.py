import streamlit as st
import google.generativeai as genai

# --- 1. SETUP & AUTH ---
st.set_page_config(page_title="Comedy Crowd Sim", page_icon="🎤", layout="wide")

api_key = st.secrets.get("api_key")
if not api_key:
    st.error("API Key not found! Check Streamlit Secrets.")
    st.stop()

genai.configure(api_key=api_key)

# --- 2. DATA ---
CROWDS = ["Underground Comedy", "The Comedy Shop", "Don't Tell", "College Gig", "Biker Bar", "VFW Hall", "Tech Mixer", "Open Mic Night", "The Woke Workshop"]
VIBES = ["Normal", "Hostile/Heckling", "Distracted", "Drunk 20-Somethings", "Passive", "New to Comedy", "Skeptical", "Jaded", "Friendly"]
STYLES = ["Observational", "Deadpan/One-Liners", "Storytelling", "Self-Deprecating", "High Energy/Physical", "Political", "Absurdist"]

# --- 3. SIDEBAR ---
with st.sidebar:
    st.title("🎤 Room Setup")
    city = st.text_input("City/Venue", value="San Luis Obispo")
    st.header("1. The Audience")
    sel_crowds = [c for c in CROWDS if st.checkbox(c, key=f"c_{c}")]
    st.header("2. The Vibe")
    sel_vibes = [v for v in VIBES if st.checkbox(v, key=f"v_{v}")]
    st.header("3. Performance Style")
    sel_styles = [s for s in STYLES if st.checkbox(s, key=f"s_{s}")]

# --- 4. MAIN ---
st.title("🎤 Comedy Crowd Sim")
st.markdown(f"**Current Stage:** Live from {city}")

bit_text = st.text_area("Paste your set here:", height=300)

if st.button("🚀 Run Simulation", use_container_width=True):
    if bit_text and sel_crowds and sel_vibes and sel_styles:
        
        # PROMPT (FIXED TRIPLE QUOTES)
        prompt = f"""
        Analyze this comedy bit for a {city} crowd.
        AUDIENCE: {', '.join(sel_crowds)}
        MOOD: {', '.join(sel_vibes)}
        STYLE: {', '.join(sel_styles)}
        
        BIT:
        {bit_text}
        
        OUTPUT:
        1. THE ROOM SOUND
        2. AUDIENCE PERSONAS
        3. SCORECARD (Laughter %, Tension %, Kill Probability %)
        4. COACH'S TIP
        """

        # TRIAGE LOGIC
        success = False
        models_to_try = ['gemini-2.0-flash', 'gemini-1.5-pro', 'gemini-1.5-flash']
        
        for m_name in models_to_try:
            if success: break
            try:
                model = genai.GenerativeModel(model_name=m_name)
                with st.spinner(f'Consulting {m_name}...'):
                    response = model.generate_content(prompt)
                    st.success(f"Showtime! Powered by {m_name}")
                    st.markdown("---")
                    st.markdown(response.text)
                    if "100%" in response.text: st.balloons()
                    success = True
            except Exception as e:
                last_error = str(e)
                continue
        
        if not success:
            st.error(f"Handshake Error: {last_error}")
    else:
        st.error("Setup incomplete! Check at least one box in every sidebar category.")
