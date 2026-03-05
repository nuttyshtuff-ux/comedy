import streamlit as st
import google.generativeai as genai

# --- 1. SETUP & AUTH ---
st.set_page_config(page_title="Comedy Crowd Sim", page_icon="🎤", layout="wide")

api_key = st.secrets.get("api_key")
if not api_key:
    st.error("API Key not found in Secrets!")
    st.stop()

genai.configure(api_key=api_key)

# --- 2. DATA CONSTANTS ---
CROWDS = [
    "Underground Comedy", "The Comedy Shop", "Don't Tell", 
    "The College Gig", "Dive Bar", "Upscale Bar", 
    "Comedy Showcase", "Open Mic Night"
]

AGES = ["Gen Z", "Millennials", "Gen X", "Boomers"]

VIBES = [
    "Normal", "Hostile/Heckling", "Distracted", "Drunk", 
    "Passive", "New to Comedy", "Skeptical but Hopeful", 
    "Jaded", "Friendly", "Silence for No Reason", 
    "Easily Offended", "Chatty"
]

STYLES = ["Observational", "One-Liners", "Storytelling", "Self-Deprecating", "Physical", "Political", "Absurdist"]

# --- 3. SIDEBAR UI ---
with st.sidebar:
    st.title("🎤 Room Setup")
    city = st.text_input("City/Venue", value="San Luis Obispo")
    
    st.header("1. The Audience")
    sel_crowds = [c for c in CROWDS if st.checkbox(c, key=f"c_{c}")]
    
    st.header("2. Age Range")
    st.caption("Who are you talking to?")
    sel_ages = [a for a in AGES if st.checkbox(a, key=f"a_{a}")]
    
    st.header("3. The Vibe")
    sel_vibes = [v for v in VIBES if st.checkbox(v, key=f"v_{v}")]
    
    st.header("4. Performance Style")
    sel_styles = [s for s in STYLES if st.checkbox(s, key=f"s_{s}")]

# --- 4. MAIN INTERFACE ---
st.title("🎤 Comedy Crowd Sim")
st.markdown(f"**Current Stage:** Live from {city}")

bit_text = st.text_area("Paste your set here:", height=300, placeholder="Paste your jokes here...")

if st.button("🚀 Run Simulation", use_container_width=True):
    if bit_text and sel_crowds and sel_ages and sel_vibes and sel_styles:
        
        models_to_try = ['gemini-2.0-flash', 'gemini-1.5-pro', 'gemini-1.5-flash']
        
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
                
                prompt = f"""
                You are a Professional Comedy Simulation Engine. 
                VENUE: {city}
                AUDIENCE TYPE: {', '.join(sel_crowds)}
                AGE RANGE: {', '.join(sel_ages)}
                MOOD: {', '.join(sel_vibes)}
                STYLE: {', '.join(sel_styles)}
                
                BIT TO ANALYZE:
                {bit_text}
                
                OUTPUT STRUCTURE:
                1. THE ROOM SOUND: (Describe background chatter and acoustics based on age and venue)
                2. AUDIENCE PERSONAS: (3 distinct reactions—make sure they match the selected AGE RANGES)
                3. GENERATIONAL CHECK: (Did the references land for this specific age mix?)
                4. SCORECARD: Laughter %, Tension %, Kill Probability %
                5. COACH'S TAGS: (Suggest 2-3 tags specifically tailored to the selected age groups)
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
        st.error("Setup incomplete! Check at least one box in every sidebar category (Audience, Age, Vibe, and Style).")
