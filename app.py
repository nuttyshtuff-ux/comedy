import streamlit as st
import google.generativeai as genai

# --- 1. SETUP & CONFIG ---
st.set_page_config(page_title="Comedy Crowd Sim", page_icon="🎤", layout="centered")

# SECURE API KEY
api_key = st.secrets.get("api_key")
if not api_key:
    st.error("API Key missing! Check your Streamlit Secrets.")
    st.stop()

# Configure the SDK
genai.configure(api_key=api_key)

# --- 2. THE COMPLETE DATASET ---
CROWD_MIX = ["Underground Comedy", "The Comedy Shop", "Don't Tell", "The College Gig", "The Biker Bar", "The VFW Hall", "The Tech Mixer", "The 'Last Resort'", "The Woke Workshop", "The Open Mic Night"]
CROWD_VIBE = ["Normal", "Hostile/Heckling", "Distracted by Sports", "Drunk 20-Somethings", "Passive", "New to Live Comedy", "Skeptical but Hopeful", "Jaded", "Actually Liking You"]
STYLES = ["Observational", "Deadpan/One-Liners", "Storytelling", "Self-Deprecating", "High Energy/Physical", "Political", "Absurdist"]

# --- 3. SIDEBAR UI ---
with st.sidebar:
    st.title("🎤 Room Setup")
    city_choice = st.text_input("Enter City or Venue", value="San Luis Obispo")
    
    st.header("1. Crowd Mix")
    sel_crowds = [c for c in CROWD_MIX if st.checkbox(c, key=f"mix_{c}")]
    
    st.header("2. Crowd Vibe")
    sel_vibes = [v for v in CROWD_VIBE if st.checkbox(v, key=f"vibe_{v}")]
    
    st.header("3. Your Style")
    sel_styles = [s for s in STYLES if st.checkbox(s, key=f"style_{s}")]

    st.divider()
    if not sel_crowds or not sel_vibes or not sel_styles:
        st.warning("⚠️ Check at least one box in each section!")

# --- 4. MAIN INTERFACE ---
st.title("🎤 Comedy Crowd Sim")
st.markdown(f"### *Live from {city_choice}...*")

bit_text = st.text_area("Paste your set here:", height=300, placeholder="Paste your bit...")

if st.button("Do the Set"):
    if bit_text and sel_crowds and sel_vibes and sel_styles:
        
        # PROMPT CONSTRUCTION
        prompt = f"""
        Analyze this comedy bit for a {city_choice} crowd.
        CROWD TYPES: {', '.join(sel_crowds)}
        MOOD: {', '.join(sel_vibes)}
        DELIVERY: {', '.join(sel_styles)}
        
        BIT: {bit_text}
        
        Provide: Room Sound, 3 Audience Personas, Scorecard, and Coach's Tip.
        """

        # TRIAGE LOGIC: Cycle through models to find the one your key allows
        # This list covers the most current stable names for 2026.
        success = False
        models_to_try = ['gemini-1.5-flash', 'gemini-1.5-pro', 'gemini-pro']
        
        last_error = ""
        for model_name in models_to_try:
            if success: break
            try:
                # Use standard generation (no beta flag unless necessary)
                model = genai.GenerativeModel(model_name)
                with st.spinner(f'Consulting {model_name}...'):
                    response = model.generate_content(prompt)
                    st.markdown("---")
                    st.markdown(response.text)
                    if "100%" in response.text: st.balloons()
                    success = True
            except Exception as e:
                last_error = str(e)
                continue
        
        if not success:
            st.error(f"Critical Failure: {last_error}")
            st.info("Since you just enabled billing, wait 3-5 minutes for Google to update your project permissions.")
    else:
        st.error("Setup incomplete!")
