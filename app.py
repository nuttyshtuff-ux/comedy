import streamlit as st
import google.generativeai as genai

# --- 1. SETUP & CONFIG ---
st.set_page_config(page_title="Comedy Crowd Sim", page_icon="🎤", layout="centered")

# SECURE API KEY
api_key = st.secrets.get("api_key", "YOUR_API_KEY_HERE")
genai.configure(api_key=api_key)

# --- 2. DATA DICTIONARIES ---
CROWD_PRESETS = {
    "The College Gig": "Gen Z, TikTok attention spans, easily offended but energetic.",
    "The Biker Bar": "Gen X, leather, zero patience, heavy drinkers.",
    "The VFW Hall": "Boomers, staring over light beer, very literal.",
    "The Tech Mixer": "Millennials, checking Slack, high-income, skeptical.",
    "The 'Last Resort'": "Tiny crowd, three guys and a mean bartender.",
    "The Woke Workshop": "Hyper-sensitive, waiting for a problematic slip-up.",
    "The Open Mic Night": "Room full of comics waiting for their own turn to talk."
}

MODIFIERS = {
    "Normal": "Standard night.",
    "Hostile/Heckling": "Aggressive, looking for a fight.",
    "Distracted by Sports": "Eyes on the TV, you have to fight for attention.",
    "High/Edibles": "Delayed reactions, giggly but confused.",
    "Passive": "Arms folded, internal laughs only.",
    "New to Live Comedy": "Don't know when to laugh, very quiet.",
    "Skeptical but Hopeful": "Warming them up is hard but possible.",
    "Jaded": "They've heard every joke before. Hard to surprise.",
    "Actually Liking You": "They want you to win."
}

CITIES = ["San Luis Obispo", "Bakersfield", "Fresno", "Santa Maria", "New York City", "Los Angeles", "Chicago", "Austin", "Nashville", "London", "Toronto", "Rural Small Town", "Las Vegas"]

STYLES = ["Observational", "Deadpan/One-Liners", "Storytelling", "Self-Deprecating", "High Energy/Physical", "Political", "Absurdist"]

# --- 3. SIDEBAR UI (Multi-Select) ---
with st.sidebar:
    st.title("🎤 Room Setup")
    
    st.header("1. Location")
    city_choice = st.selectbox("Select City", CITIES)
    
    st.header("2. Crowd Mix")
    st.caption("Select all that apply to the room:")
    selected_crowds = [c for c in CROWD_PRESETS.keys() if st.checkbox(c)]
    
    st.header("3. Crowd States")
    st.caption("What's the 'Vibe' right now?")
    selected_mods = [m for m in MODIFIERS.keys() if st.checkbox(m)]
    
    st.header("4. Performance Styles")
    st.caption("How are you delivering this set?")
    selected_styles = [s for s in STYLES if st.checkbox(s)]

    st.divider()
    if not selected_crowds or not selected_mods or not selected_styles:
        st.warning("⚠️ Please check at least one box in each section!")

# --- 4. MAIN INTERFACE ---
st.title("🎤 The Multi-Vibe Sim")
st.markdown(f"### *Simulating {city_choice}...*")

bit_text = st.text_area("Paste your bit here:", placeholder="Start typing...", height=250)

if st.button("Do the Set"):
    if bit_text and selected_crowds and selected_mods and selected_styles:
        
        # Build the descriptive strings for the AI
        crowd_desc = ", ".join(selected_crowds)
        mod_desc = ", ".join(selected_mods)
        style_desc = ", ".join(selected_styles)

        SYSTEM_PROMPT = f"""
        You are a Professional Comedy Simulation Engine. Respond as an audience in {city_choice}.
        
        THE CHALLENGE: This is a complex room.
        CROWD COMPOSITION: {crowd_desc}
        CURRENT VIBES: {mod_desc}
        PERFORMER STYLE: {style_desc}
        
        OUTPUT FORMAT:
        1. THE ROOM SOUND: (e.g. *A mix of boos and high-pitched cackling*)
        2. AUDIENCE PERSONAS: 3 distinct reactions from this specific 'hybrid' crowd.
        3. STYLE CONFLICT: How did the {style_desc} style clash or mesh with the {mod_desc} state?
        4. SCORECARD: Laughter (0-100%), Tension, and 'Kill' Probability.
        5. COACH'S TIP: One actionable sentence for this specific {city_choice} mashup.
        """
        
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        with st.spinner(f'Simulating the chaos in {city_choice}...'):
            try:
                response = model.generate_content([SYSTEM_PROMPT, bit_text])
                st.markdown("---")
                st.markdown(response.text)
                if "100%" in response.text: st.balloons()
            except Exception as e:
                st.error(f"Error: {e}. Check your Secrets!")
    else:
        st.error("Missing data! Make sure you checked at least one box in every sidebar section.")
