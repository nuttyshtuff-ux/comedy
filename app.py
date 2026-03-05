import streamlit as st
import google.generativeai as genai

# --- 1. SETUP & CONFIG ---
st.set_page_config(page_title="Comedy Crowd Sim", page_icon="🎤", layout="centered")

# SECURE API KEY
api_key = st.secrets.get("api_key", "YOUR_API_KEY_HERE")
genai.configure(api_key=api_key)

# --- 2. DATA DICTIONARIES ---
CROWD_PRESETS = {
    "The College Gig": {"size": 25, "age": "Gen Z", "vibe": "Encouraging but Naive", "desc": "TikTok attention spans."},
    "The Biker Bar": {"size": 40, "age": "Gen X", "vibe": "Drunk/Rowdy", "desc": "Leather and zero patience."},
    "The VFW Hall": {"size": 30, "age": "Boomer", "vibe": "Corporate/Cold", "desc": "Staring over light beer."},
    "The Tech Mixer": {"size": 60, "age": "Millennial", "vibe": "Corporate/Cold", "desc": "Checking Slack notifications."},
    "The 'Last Resort'": {"size": 5, "age": "Mixed", "vibe": "Drunk/Rowdy", "desc": "Three guys and a mean bartender."},
    "The Woke Workshop": {"size": 20, "age": "Gen Z", "vibe": "Encouraging but Naive", "desc": "Waiting for a 'problematic' slip-up."},
    "The Open Mic Night": {"size": 15, "age": "Mixed", "vibe": "Open Mic Comics", "desc": "Just comics waiting for their turn."}
}

MODIFIERS = {
    "Normal": "Just a standard night.",
    "Hostile/Heckling": "They are looking for a fight. One guy is already shouting 'Next!'",
    "Distracted by Sports": "The Lakers game is on. You have to be LOUD and fast.",
    "High/Edibles": "Everything is slightly delayed. Laughs are slow but deep.",
    "Passive": "The 'Arms Folded' crowd. They like you, but they won't show it.",
    "New to Live Comedy": "They don't know 'the rules.' They might talk back or be too quiet.",
    "Skeptical but Hopeful": "They've seen three bad comics tonight. Prove you're different.",
    "Jaded": "The 'Seen it all' crowd. They know every setup. Surprise them.",
    "Actually Liking You": "They want you to win. Rare, but beautiful."
}

CITIES = [
    "New York City", "Los Angeles", "Chicago", "Austin", 
    "Nashville", "London", "Toronto", "Rural Small Town", "Las Vegas"
]

# --- 3. SIDEBAR UI ---
with st.sidebar:
    st.title("🎤 Room Setup")
    
    st.header("Step 1: Location & Crowd")
    city_choice = st.selectbox("Select City", CITIES)
    base_choice = st.selectbox("Base Crowd Type", list(CROWD_PRESETS.keys()))
    selected_base = CROWD_PRESETS[base_choice]
    
    st.header("Step 2: The Twist")
    mod_choice = st.selectbox("Current State", list(MODIFIERS.keys()))
    selected_mod_desc = MODIFIERS[mod_choice]
    
    st.header("Step 3: Your Style")
    style = st.selectbox("Performance Style", [
        "Observational", "Deadpan/One-Liners", "Storytelling", "Self-Deprecating", "High Energy/Physical"
    ])

    st.divider()
    st.info(f"**Location:** {city_choice}\n\n**Vibe:** {selected_base['desc']}")

# --- 4. MAIN INTERFACE ---
st.title("🎤 The Global Crowd Sim")
st.markdown(f"### *Testing your set in {city_choice}...*")

bit_text = st.text_area("Paste your bit here:", placeholder="So, I was at the grocery store...", height=250)

if st.button("Do the Set"):
    if bit_text:
        # THE BRAIN: SYSTEM PROMPT
        SYSTEM_PROMPT = f"""
        You are a Professional Comedy Simulation Engine. 
        Respond as an audience specifically in {city_choice}.
        
        CITY CONTEXT: Adjust the reactions based on {city_choice} culture. 
        (e.g., NYC is fast-paced/cynical, Nashville is polite/religious, Rural is literal/traditional).
        
        OUTPUT FORMAT:
        1. THE ROOM SOUND: (e.g. *Scattered giggles*, *Dead silence*)
        2. AUDIENCE PERSONAS: 3 distinct reactions reflecting {city_choice} personalities.
        3. LOCAL VIBE CHECK: Did the bit feel too 'out of town' or did it resonate locally?
        4. SCORECARD: Laughter (0-100%), Tension, and 'Kill' Probability.
        5. COACH'S TIP: One actionable sentence to improve the bit for {city_choice}.
        """
        
        full_query = f"""
        STYLE: {style}
        LOCATION: {city_choice}
        CROWD: {base_choice} ({selected_base['age']})
        SIZE: {selected_base['size']} people
        MODIFIER: {selected_mod_desc}
        
        BIT:
        {bit_text}
        
        Analyze how this {style} bit lands with this {mod_choice} crowd in {city_choice}.
        """

        model = genai.GenerativeModel('gemini-1.5-flash')
        
        with st.spinner(f'Checking the room in {city_choice}...'):
            try:
                response = model.generate_content([SYSTEM_PROMPT, full_query])
                st.markdown("---")
                st.markdown(response.text)
                
                if "100%" in response.text:
                    st.balloons()
            except Exception as e:
                st.error(f"Error: {e}. Check your API Key!")
    else:
        st.warning("Type a joke first!")
