import streamlit as st
import google.generativeai as genai

# --- 1. SETUP & CONFIG ---
st.set_page_config(page_title="Comedy Crowd Sim", page_icon="🎤", layout="centered")

# SECURE API KEY
api_key = st.secrets.get("api_key")
if not api_key:
    st.error("API Key missing! Add 'api_key' to your Streamlit Secrets.")
    st.stop()

genai.configure(api_key=api_key)

# --- 2. DATA DICTIONARIES ---
CROWD_PRESETS = {
    "Underground Comedy": "Basement/DIY vibe, raw energy, hipsters and comedy nerds.",
    "The Comedy Shop (The Store)": "Historical industry pressure, 'Passed Regular' energy, high expectations.",
    "Don't Tell Comedy": "Pop-up/Secret location, attentive 'house party' vibe.",
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

STYLES = ["Observational", "Deadpan/One-Liners", "Storytelling", "Self-Deprecating", "High Energy/Physical", "Political", "Absurdist"]

# --- 3. SIDEBAR UI ---
with st.sidebar:
    st.title("🎤 Room Setup")
    city_choice = st.text_input("Enter City or Venue", value="San Luis Obispo")
    
    st.header("Crowd Mix")
    selected_crowds = [c for c in CROWD_PRESETS.keys() if st.checkbox(c)]
    
    st.header("Crowd States")
    selected_mods = [m for m in MODIFIERS.keys() if st.checkbox(m)]
    
    st.header("Performance Styles")
    selected_styles = [s for s in STYLES if st.checkbox(s)]

# --- 4. MAIN INTERFACE ---
st.title("🎤 Comedy Crowd Sim")
st.markdown(f"### *Live from {city_choice}...*")

bit_text = st.text_area("Paste your set here:", height=250)

if st.button("Do the Set"):
    if bit_text and selected_crowds and selected_mods and selected_styles:
        
        crowd_desc = ", ".join(selected_crowds)
        mod_desc = ", ".join(selected_mods)
        style_desc = ", ".join(selected_styles)

        SYSTEM_PROMPT = f"""
        You are a Comedy Simulation Engine. Respond as an audience in {city_choice}.
        CROWD: {crowd_desc} | VIBE: {mod_desc} | STYLE: {style_desc}
        
        OUTPUT:
        1. THE ROOM SOUND: (Auditory feedback)
        2. AUDIENCE PERSONAS: 3 distinct reactions.
        3. SCORECARD: Laughter (0-100%), Tension, Kill Probability.
        4. COACH'S TIP: One actionable improvement.
        """
        
        # TRIAGE LOGIC: Try models in order of likelihood to work
        success = False
        for model_name in ['gemini-1.5-pro', 'gemini-1.0-pro', 'gemini-pro']:
            if success: break
            try:
                model = genai.GenerativeModel(model_name)
                with st.spinner(f'Trying {model_name}...'):
                    response = model.generate_content([SYSTEM_PROMPT, bit_text])
                    st.markdown("---")
                    st.markdown(response.text)
                    if "100%" in response.text: st.balloons()
                    success = True
            except Exception:
                continue
        
        if not success:
            st.error("All models failed. This is usually due to an API Key that hasn't been activated for 'Pay-as-you-go' or is restricted in your region.")
    else:
        st.error("Setup incomplete! Check at least one box in every sidebar section.")h
