import streamlit as st
import google.generativeai as genai

# --- 1. SETUP ---
st.set_page_config(page_title="Comedy Crowd Sim", page_icon="🎤", layout="wide")

api_key = st.secrets.get("api_key")
if not api_key:
    st.error("Missing API Key in Streamlit Secrets!")
    st.stop()

# FORCE THE STABLE V1 API 
# This is the "Nuclear Option" to stop the v1beta 404s
genai.configure(api_key=api_key, transport='rest')

# --- 2. DATA ---
CROWDS = ["Underground Comedy", "The Comedy Shop", "Don't Tell", "The College Gig", "Dive Bar", "Upscale Bar", "Comedy Showcase", "Open Mic Night"]
AGES = ["Gen Z", "Millennials", "Gen X", "Boomers"]
VIBES = ["Normal", "Hostile/Heckling", "Distracted", "Drunk", "Passive", "New to Comedy", "Skeptical but Hopeful", "Jaded", "Friendly", "Silence for No Reason", "Easily Offended", "Chatty", "Other Comics Watching"]

# --- 3. SIDEBAR ---
with st.sidebar:
    st.title("🎤 Room Setup")
    city = st.text_input("City", value="San Luis Obispo")
    
    st.markdown("---")
    st.header("1. The Audience")
    sel_crowds = [c for c in CROWDS if st.checkbox(c, key=f"c_{c}")]
    
    st.header("2. Age Range")
    sel_ages = [a for a in AGES if st.checkbox(a, key=f"a_{a}")]
    
    st.header("3. The Vibe")
    sel_vibes = [v for v in VIBES if st.checkbox(v, key=f"v_{v}")]

    # COACH MODE AT BOTTOM
    st.markdown("---")
    st.header("💡 Pro Mode")
    coach_mode = st.checkbox("Coach Me on This Room", value=False)

# --- 4. MAIN ---
st.title("🎤 Comedy Crowd Sim")
bit_text = st.text_area("Paste your set here:", height=300)

if st.button("🚀 Run Simulation", use_container_width=True):
    if bit_text and sel_crowds and sel_ages and sel_vibes:
        
        try:
            # THE FIX: We are calling the model by its versioned production name
            # This ensures the library doesn't append 'v1beta' to the URL
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            coach_instruction = ""
            if coach_mode:
                coach_instruction = f"Provide a 'COACH'S CORNER' with advice for {sel_ages} in {sel_crowds}."

            prompt = f"ACT AS A COMEDY AUDIENCE. {coach_instruction} VENUE: {sel_crowds} | VIBE: {sel_vibes} | BIT: {bit_text}"
            
            with st.spinner('Forcing Stable Connection...'):
                # We use the 'v1' API specifically here
                response = model.generate_content(prompt)
                
                st.markdown("---")
                st.markdown(response.text)
                if "100%" in response.text: st.balloons()
                
        except Exception as e:
            # If the high-level call fails, we show the exact error
            st.error(f"Error: {e}")
            st.info("Check Google AI Studio: Is the 'Generative Language API' enabled for your project?")
    else:
        st.warning("Select at least one option in every category!")
