import streamlit as st
import google.generativeai as genai

# --- 1. SETUP & CONFIG ---
st.set_page_config(page_title="Comedy Crowd Sim", page_icon="🎤", layout="centered")

# SECURE API KEY
api_key = st.secrets.get("api_key")
if not api_key:
    st.error("API Key missing! Check your Streamlit Secrets.")
    st.stop()

genai.configure(api_key=api_key)

# --- 2. DATA ---
CROWD_MIX = ["Underground Comedy", "The Comedy Shop", "Don't Tell", "College Gig", "Biker Bar", "VFW Hall", "Tech Mixer", "Open Mic"]
CROWD_VIBE = ["Normal", "Hostile", "Drunk 20s", "Passive", "Jaded", "Friendly"]
STYLES = ["Observational", "One-Liners", "Storytelling", "Self-Deprecating", "Physical", "Political"]

# --- 3. SIDEBAR (Rebuilt for Stability) ---
with st.sidebar:
    st.title("🎤 Room Setup")
    city = st.text_input("City/Venue", value="San Luis Obispo")
    
    st.header("1. Crowd Mix")
    sel_crowds = []
    for c in CROWD_MIX:
        if st.checkbox(c, key=f"mix_{c}"):
            sel_crowds.append(c)
            
    st.header("2. Crowd Vibe")
    sel_vibes = []
    for v in CROWD_VIBE:
        if st.checkbox(v, key=f"vibe_{v}"):
            sel_vibes.append(v)
            
    st.header("3. Your Style")
    sel_styles = []
    for s in STYLES:
        if st.checkbox(s, key=f"style_{s}"):
            sel_styles.append(s)

# --- 4. MAIN INTERFACE ---
st.title("🎤 Comedy Crowd Sim")
st.markdown(f"### *Live from {city}...*")

bit_text = st.text_area("Paste your set here:", height=250, placeholder="Type or paste your jokes here...")

if st.button("Run Simulation"):
    if bit_text and sel_crowds and sel_vibes and sel_styles:
        # 2026 STABLE MODELS
        models_to_try = ['gemini-2.0-flash', 'gemini-1.5-pro', 'gemini-1.5-flash']
        
        success = False
        last_error = ""
        
        for m_name in models_to_try:
            if success: break
            try:
                model = genai.GenerativeModel(m_name)
                prompt = f"Simulate a {city} audience reaction. Crowd: {sel_crowds}. Vibe: {sel_vibes}. Style: {sel_styles}. BIT: {bit_text}"
                
                with st.spinner(f'Consulting {m_name}...'):
                    response = model.generate_content(prompt)
                    st.markdown("---")
                    st.markdown(response.text)
                    if "100%" in response.text: st.balloons()
                    success = True
            except Exception as e:
                last_error = str(e)
                continue
        
        if not success:
            st.error(f"Models are still syncing: {last_error}")
    else:
        st.warning("⚠️ Setup incomplete! Please check at least one box in every sidebar category (Mix, Vibe, and Style).")
