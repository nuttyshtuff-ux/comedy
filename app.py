import streamlit as st
import google.generativeai as genai

# --- 1. SETUP & AUTH ---
st.set_page_config(page_title="Comedy Crowd Sim", page_icon="🎤", layout="wide")

# Retrieve the key from Secrets
api_key = st.secrets.get("api_key")
if not api_key:
    st.error("API Key not found in Streamlit Secrets! Check your dashboard.")
    st.stop()

genai.configure(api_key=api_key)

# --- 2. DATA CONSTANTS ---
CROWDS = ["Underground Comedy", "The Comedy Shop", "Don't Tell", "College Gig", "Biker Bar", "VFW Hall", "Tech Mixer", "Open Mic Night"]
VIBES = ["Normal", "Hostile/Heckling", "Distracted", "Drunk 20-Somethings", "Passive", "New to Comedy", "Skeptical", "Jaded", "Friendly"]
STYLES = ["Observational", "One-Liners", "Storytelling", "Self-Deprecating", "Physical", "Political", "Absurdist"]

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

bit_text = st.text_area("Paste your set here:", height=300, placeholder="Enter your jokes here...")

if st.button("🚀 Run Simulation", use_container_width=True):
    if bit_text and sel_crowds and sel_vibes and sel_styles:
        
        # TIER 1 SUCCESSION PLAN
        # Since you're Tier 1, Pro 1.5 is your best bet for nuanced comedy feedback
        models_to_try = ['gemini-1.5-pro', 'gemini-1.5-flash', 'gemini-pro']
        
        # Safety: BLOCK_NONE allows edgy comedy content
        safety = [
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
        ]
        
        success = False
        for m_name in models_to_try:
            if success: break
            try:
                model = genai.GenerativeModel(model_name=m_name, safety_settings=safety)
                
                prompt = f"""
                You are a Comedy Crowd Simulator.
                VENUE: {city}
                AUDIENCE TYPE: {', '.join(sel_crowds)}
                CURRENT MOOD: {', '.join(sel_vibes)}
                COMIC STYLE: {', '.join(sel_styles)}
                
                THE BIT:
                {bit_text}
                
                RESPONSE FORMAT:
                - ROOM SOUND: (Describe the auditory vibe)
                - LOCAL PERSONAS: (3 specific SLO-style audience reactions)
                - ANALYSIS: (How the jokes landed given the crowd's mood)
                - SCORECARD: Laughter %, Tension %, Kill Probability %
                - COACH'S TIP: (One actionable way to improve the set)
                """
                
                with st.spinner(f'Consulting {m_name}...'):
                    response = model.generate_content(prompt)
                    st.success(f"Response generated via {m_name}")
                    st.markdown("---")
                    st.markdown(response.text)
                    if "100%" in response.text: st.balloons()
                    success = True
            except Exception as e:
                st.warning(f"Note: {m_name} is still initializing or restricted. Trying fallback...")
                last_error = e
                continue
        
        if not success:
            st.error(f"Critical Error: {last_error}")
            st.info("Check your Google AI Studio dashboard. If it says 'Tier 1,' make sure your billing account is active and try creating a NEW API key.")
    else:
        st.error("Please fill out all categories in the sidebar and paste your bit!")
