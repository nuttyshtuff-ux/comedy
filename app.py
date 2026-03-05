import streamlit as st
import google.generativeai as genai

# --- 1. SETUP & CONFIG ---
st.set_page_config(page_title="Comedy Crowd Sim", page_icon="🎤", layout="centered")

# Retrieve API key from Streamlit Secrets
api_key = st.secrets.get("api_key")
if not api_key:
    st.error("API Key missing! Check your Streamlit Secrets tab.")
    st.stop()

genai.configure(api_key=api_key)

# --- 2. THE COMPLETE DATASET ---
CROWD_MIX = [
    "Underground Comedy", "The Comedy Shop", "Don't Tell", 
    "The College Gig", "The Biker Bar", "The VFW Hall", 
    "The Tech Mixer", "The 'Last Resort'", "The Woke Workshop", "The Open Mic Night"
]

CROWD_VIBE = [
    "Normal", "Hostile/Heckling", "Distracted by Sports", 
    "Drunk 20-Somethings", "Passive", "New to Live Comedy", 
    "Skeptical but Hopeful", "Jaded", "Actually Liking You"
]

STYLES = [
    "Observational", "Deadpan/One-Liners", "Storytelling", 
    "Self-Deprecating", "High Energy/Physical", "Political", "Absurdist"
]

# --- 3. SIDEBAR UI ---
with st.sidebar:
    st.title("🎤 Room Setup")
    city_choice = st.text_input("Enter City or Venue", value="San Luis Obispo")
    
    st.header("1. Crowd Mix")
    st.caption("Who is in the room?")
    sel_crowds = [c for c in CROWD_MIX if st.checkbox(c, key=f"mix_{c}")]
    
    st.header("2. Crowd Vibe")
    st.caption("What's the energy?")
    sel_vibes = [v for v in CROWD_VIBE if st.checkbox(v, key=f"vibe_{v}")]
    
    st.header("3. Your Style")
    st.caption("How are you delivering it?")
    sel_styles = [s for s in STYLES if st.checkbox(s, key=f"style_{s}")]

    st.divider()
    if not sel_crowds or not sel_vibes or not sel_styles:
        st.warning("⚠️ Check at least one box in each section!")

# --- 4. MAIN INTERFACE ---
st.title("🎤 Comedy Crowd Sim")
st.markdown(f"### *Live from {city_choice}...*")

bit_text = st.text_area("Paste your set here:", height=300, placeholder="Type or paste your jokes here...")

if st.button("Do the Set"):
    if bit_text and sel_crowds and sel_vibes and sel_styles:
        
        # We'll use the 1.5-pro model for the most nuanced feedback
        model_name = 'gemini-1.5-pro'
        
        # Safety settings to allow edgy/comedy content
        safety_settings = [
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
        ]

        try:
            model = genai.GenerativeModel(model_name=model_name, safety_settings=safety_settings)
            
            prompt = f"""
            SYSTEM: You are a Professional Comedy Simulation Engine. 
            Respond as a live audience in {city_choice}.
            
            ROOM CONTEXT:
            - Crowd Types: {', '.join(sel_crowds)}
            - Audience Mood: {', '.join(sel_vibes)}
            - Performer Style: {', '.join(sel_styles)}
            
            BIT TO ANALYZE:
            {bit_text}
            
            OUTPUT FORMAT:
            1. THE ROOM SOUND: (Describe the literal noise in the room)
            2. AUDIENCE PERSONAS: Provide 3 distinct, local reactions.
            3. PERFORMANCE ANALYSIS: How did the {', '.join(sel_styles)} approach land?
            4. SCORECARD: Laughter (0-100%), Tension, Kill Probability.
            5. COACH'S TIP: One actionable sentence to make this bit 'kill' in {city_choice}.
            """
            
            with st.spinner(f'Analyzing the room...'):
                response = model.generate_content(prompt)
                st.markdown("---")
                st.markdown(response.text)
                if "100%" in response.text:
                    st.balloons()
                    
        except Exception as e:
            st.error(f"Error: {e}")
            st.info("If you just enabled billing, it may take a few minutes for the models to unlock.")
    else:
        st.error("Setup incomplete! Please check your sidebar selections.")
