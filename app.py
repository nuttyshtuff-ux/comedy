import streamlit as st
import google.generativeai as genai

# --- 1. SETUP & CONFIG ---
st.set_page_config(page_title="Comedy Crowd Sim", page_icon="🎤", layout="centered")

api_key = st.secrets.get("api_key")
if not api_key:
    st.error("API Key missing! Check Streamlit Secrets.")
    st.stop()

genai.configure(api_key=api_key)

# --- 2. DATA ---
CROWD_MIX = ["Underground Comedy", "The Comedy Shop", "Don't Tell", "College Gig", "Biker Bar", "VFW Hall", "Tech Mixer", "Open Mic"]
CROWD_VIBE = ["Normal", "Hostile", "Drunk 20s", "Passive", "Jaded", "Friendly"]
STYLES = ["Observational", "One-Liners", "Storytelling", "Self-Deprecating", "Physical", "Political"]

# --- 3. SIDEBAR ---
with st.sidebar:
    st.title("🎤 Room Setup")
    city = st.text_input("City/Venue", value="San Luis Obispo")
    sel_crowds = [c for c in CROWD_MIX if st.checkbox(c)]
    sel_vibes = [v for v in CROWD_VIBE if st.checkbox(v)]
    sel_styles = [s for s in STYLES if st.checkbox(s)]

# --- 4. MAIN ---
st.title("🎤 Comedy Crowd Sim")
bit_text = st.text_area("Paste your set here:", height=250)

if st.button("Run Simulation"):
    if bit_text and sel_crowds and sel_vibes and sel_styles:
        
        # 2026 STABLE MODELS
        # Note: 'gemini-2.5-flash' is the new industry standard
        models_to_try = ['gemini-2.5-flash', 'gemini-2.5-pro', 'gemini-2.0-flash']
        
        success = False
        for m_name in models_to_try:
            try:
                model = genai.GenerativeModel(m_name)
                prompt = f"Simulate a {city} audience reaction. Crowd: {sel_crowds}. Vibe: {sel_vibes}. Style: {sel_styles}. BIT: {bit_text}"
                
                with st.spinner(f'Opening doors for {m_name}...'):
                    response = model.generate_content(prompt)
                    st.markdown("---")
                    st.markdown(response.text)
                    success = True
                    break
            except Exception:
                continue
        
        if not success:
            st.error("Model Handshake Failed.")
            st.write("### Diagnostic: Your Key supports these models:")
            try:
                # This lists what your SPECIFIC key is allowed to do
                available = [m.name.replace('models/', '') for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
                st.write(available)
            except:
                st.write("Could not retrieve model list. Check your billing status at ai.google.dev.")
    else:
        st.error("Select at least one checkbox in each category!")
