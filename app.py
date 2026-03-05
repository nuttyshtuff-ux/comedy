import streamlit as st
import google.generativeai as genai

# --- 1. SETUP & CONFIG ---
st.set_page_config(page_title="Comedy Crowd Sim", page_icon="🎤", layout="centered")

# Retrieve API key from Streamlit Secrets
api_key = st.secrets.get("api_key")
if not api_key:
    st.error("API Key missing! Add 'api_key' to your Secrets on the Streamlit dashboard.")
    st.stop()

genai.configure(api_key=api_key)

# --- 2. DATA DICTIONARIES ---
CROWD_PRESETS = {
    "Underground Comedy": "Basement/DIY vibe, raw energy, hipsters and comedy nerds.",
    "The Comedy Shop (The Store)": "Industry pressure, 'Passed Regular' energy, high expectations.",
    "Don't Tell Comedy": "Pop-up location, attentive 'house party' vibe, very supportive.",
    "The College Gig": "Gen Z, TikTok attention spans, energetic.",
    "The Biker Bar": "Gen X, leather, zero patience, heavy drinkers.",
    "The VFW Hall": "Boomers, staring over light beer, very literal.",
    "The Tech Mixer": "Millennials, checking Slack, high-income.",
    "The 'Last Resort'": "Tiny crowd, three guys and a mean bartender.",
    "The Woke Workshop": "Hyper-sensitive, waiting for a problematic slip-up.",
    "The Open Mic Night": "Room full of comics waiting for their turn."
}

MODIFIERS = {
    "Normal": "Standard night.",
    "Hostile/Heckling": "Aggressively seeking a reason to boo.",
    "Distracted by Sports": "Eyes on the TV; you have to fight for attention.",
    "Drunk 20-Somethings": "Rowdy, shouting out, high volume but short attention spans.",
    "Passive": "The 'Arms Folded' crowd. Internal laughs only.",
    "New to Live Comedy": "Don't know the etiquette; might be too quiet.",
    "Skeptical but Hopeful": "They've seen bad acts; prove you aren't one.",
    "Jaded": "They know every setup; hard to surprise.",
    "Actually Liking You": "A rare 'Friendly' room."
}

STYLES = ["Observational", "One-Liners", "Storytelling", "Self-Deprecating", "High Energy/Physical", "Political", "Absurdist"]

# --- 3. SIDEBAR UI ---
with st.sidebar:
    st.title("🎤 Room Setup")
    city_choice = st.text_input("Enter City or Venue", value="San Luis Obispo")
    
    st.header("1. Crowd Mix")
    selected_crowds = [c for c in CROWD_PRESETS.keys() if st.checkbox(c)]
    
    st.header("2. Crowd States")
    selected_mods = [m for m in MODIFIERS.keys() if st.checkbox(m)]
    
    st.header("3. Performance Styles")
    selected_styles = [s for s in STYLES if st.checkbox(s)]

    st.divider()
    if not selected_crowds or not selected_mods or not selected_styles:
        st.warning("⚠️ Select at least one item in each category!")

# --- 4. MAIN INTERFACE ---
st.title("🎤 Comedy Crowd Sim")
st.markdown(f"### *Live from {city_choice}...*")

bit_text = st.text_area("Paste your set here:", height=250)

if st.button("Do the Set"):
    if bit_text and selected_crowds and selected_mods and selected_styles:
        
        # Build prompt context
        crowd_info = ", ".join(selected_crowds)
        vibe_info = ", ".join(selected_mods)
        style_info = ", ".join(selected_styles)

        SYSTEM_PROMPT = f"""
        You are a Professional Comedy Simulation Engine. Respond as an audience in {city_choice}.
        CROWD: {crowd_info} | VIBE: {vibe_info} | STYLE: {style_info}
        
        OUTPUT FORMAT:
        1. THE ROOM SOUND: (Auditory feedback)
        2. AUDIENCE PERSONAS: 3 distinct reactions from {city_choice} locals.
        3. SCORECARD: Laughter (0-100%), Tension, Kill Probability.
        4. COACH'S TIP: One actionable improvement.
        """

        # SAFETY FILTERS: Set to BLOCK_NONE to ensure jokes land
        safety_settings = [
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
        ]

        # TRIAGE LOGIC: Try models in order of current 2026 support
        success = False
        models_to_try = ['gemini-2.0-flash', 'gemini-1.5-pro', 'gemini-1.5-flash']
        
        for model_name in models_to_try:
            if success: break
            try:
                model = genai.GenerativeModel(model_name=model_name, safety_settings=safety_settings)
                with st.spinner(f'Checking the room via {model_name}...'):
                    response = model.generate_content([SYSTEM_PROMPT, bit_text])
                    st.markdown("---")
                    st.markdown(response.text)
                    if "100%" in response.text: st.balloons()
                    success = True
            except Exception:
                continue
        
        if not success:
            st.error("All models failed. Check your API key and Ensure billing is enabled at ai.google.dev.")
    else:
        st.error("Setup incomplete! Check at least one box in every sidebar section.")
