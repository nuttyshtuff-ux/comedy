import streamlit as st
import google.generativeai as genai

# --- 1. SETUP & AUTH ---
st.set_page_config(page_title="Comedy Crowd Sim", page_icon="🎤", layout="wide")

api_key = st.secrets.get("api_key")
if not api_key:
    st.error("API Key not found in Secrets! Please add your Tier 1 key.")
    st.stop()

genai.configure(api_key=api_key)

# --- 2. DATA CONSTANTS ---
CROWDS = ["Underground Comedy", "The Comedy Shop", "Don't Tell", "College Gig", "Biker Bar", "VFW Hall", "Tech Mixer", "Open Mic Night", "The Woke Workshop"]
VIBES = ["Normal", "Hostile/Heckling", "Distracted", "Drunk 20-Somethings", "Passive", "New to Comedy", "Skeptical", "Jaded", "Friendly"]
STYLES = ["Observational", "One-Liners", "Storytelling", "Self-Deprecating", "High Energy/Physical", "Political", "Absurdist"]

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

bit_text = st.text_area("Paste your set here:", height=300, placeholder="Paste your jokes here for analysis...")

if st.button("🚀 Run Simulation", use_container_width=True):
    if bit_text and sel_crowds and sel_vibes and sel_styles:
        
        # TIER 1 STABLE MODELS
        models_to_try = ['gemini-2.0-flash', 'gemini-1.5-pro', 'gemini-1.5-flash']
        
        # Safety: BLOCK_NONE allows for edgy comedy content
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
                model = genai.GenerativeModel(model_name=m_name, safety_settings=safety)
                
                # High-level prompt for nuanced comedy feedback
                prompt = f"""
                You are an expert Comedy Coach and Audience Simulator.
                VENUE: {city}
                AUDIENCE: {', '.join(sel_crowds)}
                MOOD: {', '.join(sel_vibes)}
                STYLE: {', '.join(sel_styles)}
                
                BIT TO ANALYZE:
                {bit_text}
                
                RESPONSE STRUCTURE:
                1. THE ROOM SOUND: Describe the literal atmosphere and noise level.
                2. THE AUDIENCE PERSONAS: Give 3 specific examples of how different people in the crowd react.
                3. THE 'VIBRATION' CHECK: Analyze the energy level—where does it peak and where does it dip?
                4. PERFORMANCE SCORECARD:
                   - Laughter: (0-100%)
                   - Tension: (0-100%)
                   - Kill Probability: (0-100%)
                5. COACH'S TAGS: Suggest 2-3 specific 'tags' (short follow-up jokes) to make the bit stronger.
                """
                
                with st.spinner(f'Opening the room with {m_name}...'):
                    response = model.generate_content(prompt)
                    st.success(f"Simulation Complete (via {m_name})")
                    st.markdown("---")
                    st.markdown(response.text)
                    if "100%" in response.text: st.balloons()
                    success = True
            except Exception as e:
                last_error = str(e)
                continue
        
        if not success:
            st.error(f"System Error: {last_error}")
    else:
        st.error("Setup incomplete! Check at least one box in every sidebar category.")
