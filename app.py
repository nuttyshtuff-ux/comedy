import streamlit as st
import google.generativeai as genai

# --- 1. SETUP & CONFIG ---
st.set_page_config(page_title="Comedy Crowd Sim", page_icon="🎤", layout="centered")

# SECURE API KEY (Pulls from Streamlit Cloud Secrets)
api_key = st.secrets.get("api_key", "YOUR_API_KEY_HERE")
genai.configure(api_key=api_key)

# --- 2. DATA DICTIONARIES ---
CROWD_PRESETS = {
    "Underground Comedy": "Basement/DIY vibe, raw energy, hipsters and comedy nerds.",
    "The Comedy Shop (The Store)": "Historical industry pressure, 'Passed Regular' energy, high expectations.",
    "Don't Tell Comedy": "Pop-up/Secret location, attentive 'house party' vibe, very supportive.",
    "The College Gig": "Gen Z, TikTok attention spans, energetic.",
    "The Biker Bar": "Gen X, leather, zero patience, heavy drinkers.",
    "The VFW Hall": "Boomers, staring over light beer, very literal.",
    "The Tech Mixer": "Millennials, checking Slack, high-income, skeptical.",
    "The 'Last Resort'": "Tiny crowd, three guys and a mean bartender.",
    "The Woke Workshop": "Hyper-sensitive, waiting for a problematic slip-up.",
    "The Open Mic Night": "Room full of comics waiting for their own turn to talk."
}

MODIFIERS = {
    "Normal": "Standard night.",
    "Hostile/Heckling": "Aggressively seeking a reason to boo.",
    "Distracted by Sports": "Eyes on the TV; you have to fight for every look.",
    "Drunk 20-Somethings": "Rowdy, shouting out, high volume laughs but short attention spans.",
    "Passive": "The 'Arms Folded' crowd. Internal laughs only.",
    "New to Live Comedy": "Don't know the etiquette; might be too quiet or talkative.",
    "Skeptical but Hopeful": "They've seen bad acts tonight; prove you aren't one.",
    "Jaded": "They know every setup; hard to surprise.",
    "Actually Liking You": "A rare 'Friendly' room."
}

STYLES = ["Observational", "Deadpan/One-Liners", "Storytelling", "Self-Deprecating", "High Energy/Physical", "Political", "Absurdist"]

# --- 3. SIDEBAR UI ---
with st.sidebar:
    st.title("🎤 Room Setup")
    
    st.header("1. Location")
    city_choice = st.text_input("Enter City or Venue", value="San Luis Obispo")
    
    st.header("2. Crowd Mix")
    selected_crowds = [c for c in CROWD_PRESETS.keys() if st.checkbox(c)]
    
    st.header("3. Crowd States")
    selected_mods = [m for m in MODIFIERS.keys() if st.checkbox(m)]
    
    st.header("4. Performance Styles")
    selected_styles = [s for s in STYLES if st.checkbox(s)]

    st.divider()
    if not selected_crowds or not selected_mods or not selected_styles:
        st.warning("⚠️ Select at least one item in each category!")

# --- 4. MAIN INTERFACE ---
st.title("🎤 Comedy Crowd Sim")
st.markdown(f"### *Simulating a set in {city_choice}...*")

bit_text = st.text_area("Paste your set here:", placeholder="Paste your bits...", height=250)

if st.button("Do the Set"):
    if bit_text and selected_crowds and selected_mods and selected_styles:
        
        crowd_desc = ", ".join(selected_crowds)
        mod_desc = ", ".join(selected_mods)
        style_desc = ", ".join(selected_styles)

        SYSTEM_PROMPT = f"""
        You are a Professional Comedy Simulation Engine. Respond as an audience in {city_choice}.
        CROWD: {crowd_desc} | VIBE: {mod_desc} | STYLE: {style_desc}
        
        OUTPUT:
        1. THE ROOM SOUND: (Literal auditory feedback)
        2. AUDIENCE PERSONAS: 3 distinct reactions.
        3. LOCAL VIBE CHECK: Specific to {city_choice}.
        4. SCORECARD: Laughter (0-100%), Tension, Kill Probability.
        5. COACH'S TIP: One actionable improvement.
        """
        
        # UPDATED MODEL STRING TO FIX 404 ERROR
        model = genai.GenerativeModel('models/gemini-1.5-flash')
        
        with st.spinner(f'Checking the room in {city_choice}...'):
            try:
                response = model.generate_content([SYSTEM_PROMPT, bit_text])
                st.markdown("---")
                st.markdown(response.text)
                if "100%" in response.text: st.balloons()
            except Exception as e:
                # Better error reporting
                st.error(f"Error: {e}")
                st.info("Check if your API Key is correct in the Secrets tab (three dots menu -> Settings -> Secrets).")
    else:
        st.error("Setup incomplete!")
