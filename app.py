import streamlit as st
import google.generativeai as genai

# --- 1. SETUP & CONFIG ---
st.set_page_config(page_title="Comedy Crowd Sim", page_icon="🎤", layout="centered")

# Retrieve API key
api_key = st.secrets.get("api_key")
if not api_key:
    st.error("API Key missing! Check your Streamlit Secrets.")
    st.stop()

genai.configure(api_key=api_key)

# --- 2. DATA ---
CROWD_PRESETS = {
    "Underground Comedy": "Basement vibe, raw energy, hipsters/nerds.",
    "The Comedy Shop (The Store)": "Industry pressure, pitch-black room, high expectations.",
    "Don't Tell Comedy": "Pop-up/Secret location, focused house-party vibe.",
    "The College Gig": "Gen Z, TikTok attention spans, energetic.",
    "The Biker Bar": "Gen X, leather, heavy drinkers, zero patience.",
    "The VFW Hall": "Boomers, staring over light beer, very literal.",
    "The Tech Mixer": "Millennials, checking Slack, skeptical.",
    "The 'Last Resort'": "Three guys and a mean bartender.",
    "The Woke Workshop": "Hyper-sensitive, waiting for a slip-up.",
    "The Open Mic Night": "Comics waiting for their turn."
}

MODIFIERS = {
    "Normal": "Standard night.",
    "Hostile/Heckling": "Aggressively seeking a reason to boo.",
    "Distracted by Sports": "Eyes on the TV; you have to fight for attention.",
    "Drunk 20-Somethings": "Rowdy, shouting out, loud but short attention spans.",
    "Passive": "Arms folded, internal laughs only.",
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

# --- 4. MAIN INTERFACE ---
st.title("🎤 Comedy Crowd Sim")
st.markdown(f"### *Live from {city_choice}...*")

bit_text = st.text_area("Paste your set here:", placeholder="Paste your bit...", height=250)

if st.button("Do the Set"):
    if bit_text and selected_crowds and selected_mods and selected_styles:
        
        crowd_desc = ", ".join(selected_crowds)
        mod_desc = ", ".join(selected_mods)
        style_desc = ", ".join(selected_styles)

        SYSTEM_PROMPT = f"Analyze this comedy bit for a {city_choice} crowd. CROWD: {crowd_desc}. VIBE: {mod_desc}. STYLE: {style_desc}. Provide: 1. Room Sound, 2. Audience Personas, 3. Scorecard (Laughter/Kill Prob), 4. Coach's Tip."

        # SAFETY SETTINGS
        safety_settings = [
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
        ]

        # TRIAGE LOGIC: Try every possible model name variation
        success = False
        # These are the most common supported strings for billing-enabled keys
        models_to_try = ['gemini-1.5-flash', 'gemini-1.5-pro', 'gemini-pro']
        
        last_error = ""
        for model_name in models_to_try:
            if success: break
            try:
                model = genai.GenerativeModel(model_name=model_name, safety_settings=safety_settings)
                with st.spinner(f'Trying {model_name}...'):
                    response = model.generate_content([SYSTEM_PROMPT, bit_text])
                    st.markdown("---")
                    st.markdown(response.text)
                    if "100%" in response.text: st.balloons()
                    success = True
            except Exception as e:
                last_error = str(e)
                continue
        
        if not success:
            st.error(f"Models are still activating: {last_error}")
            st.info("Wait 2 minutes and try again. Google is currently linking your billing to the API models.")
    else:
        st.error("Setup incomplete!")
