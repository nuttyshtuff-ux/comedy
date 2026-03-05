import streamlit as st
import google.generativeai as genai

# --- 1. SETUP & AUTH ---
st.set_page_config(page_title="Comedy Crowd Sim", page_icon="🎤", layout="wide")

api_key = st.secrets.get("api_key")
if not api_key:
    st.error("API Key missing! Check Streamlit Secrets.")
    st.stop()

genai.configure(api_key=api_key)

# --- 2. DATA ---
CROWDS = ["Underground Comedy", "The Comedy Shop", "Don't Tell", "The College Gig", "Dive Bar", "Upscale Bar", "Comedy Showcase", "Open Mic Night"]
AGES = ["Gen Z", "Millennials", "Gen X", "Boomers"]
VIBES = ["Normal", "Hostile/Heckling", "Distracted", "Drunk", "Passive", "New to Comedy", "Skeptical but Hopeful", "Jaded", "Friendly", "Silence for No Reason", "Easily Offended", "Chatty"]

# --- 3. SIDEBAR ---
with st.sidebar:
    st.title("🎤 Room Setup")
    city = st.text_input("City/Venue", value="San Luis Obispo")
    
    st.header("1. The Audience")
    sel_crowds = [c for c in CROWDS if st.checkbox(c, key=f"c_{c}")]
    
    st.header("2. Age Range")
    sel_ages = [a for a in AGES if st.checkbox(a, key=f"a_{a}")]
    
    st.header("3. The Vibe")
    sel_vibes = [v for v in VIBES if st.checkbox(v, key=f"v_{v}")]

# --- 4. MAIN ---
st.title("🎤 Comedy Crowd Sim")
st.markdown(f"**Current Stage:** Live from {city}")

bit_text = st.text_area("Paste your set here:", height=300, placeholder="The AI will simulate the room and tell you if it actually lands...")

if st.button("🚀 Run Simulation", use_container_width=True):
    if bit_text and sel_crowds and sel_ages and sel_vibes:
        
        # Use the most robust stable model for Tier 1
        model_name = 'gemini-2.0-flash'
        
        # Safety settings (BLOCK_NONE allows for edgy comedy content)
        safety = [
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
        ]
        
        try:
            model = genai.GenerativeModel(model_name=model_name, safety_settings=safety)
            
            prompt = f"""
            You are a Professional Comedy Simulation Engine.
            VENUE: {city} | AUDIENCE: {', '.join(sel_crowds)} | AGES: {', '.join(sel_ages)} | VIBE: {', '.join(sel_vibes)}
            
            BIT:
            {bit_text}
            
            RESPONSE STRUCTURE:
            1. THE ROOM SOUND: (Literal background noise, laughter levels, or awkward silence)
            2. AUDIENCE PERSONAS: (3 distinct reactions—who laughed, who stared, and who checked their phone?)
            3. WHY IT LANDED (OR FAILED): (A blunt assessment of the humor based on the generational and venue context.)
            4. SCORECARD: Laughter %, Tension %, Kill Probability %
            5. THE TAG: (Suggest one short, sharp 'tag' to save or boost the bit.)
            """
            
            with st.spinner(f'Consulting {model_name}...'):
                response = model.generate_content(prompt)
                st.markdown("---")
                st.markdown(response.text)
                if "100%" in response.text: st.balloons()
        except Exception as e:
            st.error(f"System Error: {e}")
            st.info("Since you just upgraded to Tier 1, ensure your billing account is active in Google Cloud Console.")
    else:
        st.error("Setup incomplete! Select at least one Audience, Age, and Vibe.")
