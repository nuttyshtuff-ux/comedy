import streamlit as st
import google.generativeai as genai

# --- 1. SETUP ---
st.set_page_config(page_title="Comedy Crowd Sim", page_icon="🎤")

api_key = st.secrets.get("api_key")
if not api_key:
    st.error("Missing API Key in Streamlit Secrets!")
    st.stop()

# FORCE CONFIGURATION
genai.configure(api_key=api_key)

# --- 2. THE UI ---
with st.sidebar:
    st.title("🎤 Room Setup")
    city = st.text_input("City", "San Luis Obispo")
    
    st.header("1. The Audience")
    # Simplified to multiselect for reliability
    sel_crowds = st.multiselect("Venue", ["Underground", "The Store", "College Gig", "Dive Bar", "Upscale Bar", "Comedy Showcase"])
    
    st.header("2. Age Range")
    sel_ages = st.multiselect("Ages", ["Gen Z", "Millennials", "Gen X", "Boomers"])
    
    st.header("3. The Vibe")
    sel_vibes = st.multiselect("Vibe", ["Normal", "Hostile", "Drunk", "Friendly", "Silence", "Comics Watching"])

st.title("🎤 Is It Funny?")
bit_text = st.text_area("Paste your set here:", height=300)

if st.button("🚀 Run Simulation", use_container_width=True):
    if bit_text and sel_crowds and sel_ages and sel_vibes:
        # THE FIX: Explicitly call the model WITHOUT the 'models/' prefix
        # We try 'gemini-1.5-flash' first as it is the most robust for v1 stable
        try:
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            prompt = f"""
            Analyze this comedy bit for a {city} crowd.
            AUDIENCE: {sel_crowds} | AGES: {sel_ages} | VIBE: {sel_vibes}
            BIT: {bit_text}
            
            RESPONSE:
            1. THE ROOM SOUND
            2. AUDIENCE PERSONAS
            3. IS IT FUNNY? (Blunt assessment)
            4. SCORECARD (Laughter %, Tension %, Kill Probability %)
            5. THE TAG
            """
            
            with st.spinner('Opening the room...'):
                # We do NOT use the 'v1beta' endpoint here
                response = model.generate_content(prompt)
                st.markdown("---")
                st.markdown(response.text)
                
        except Exception as e:
            # If Flash fails, we try the Pro version
            try:
                model_pro = genai.GenerativeModel('gemini-1.5-pro')
                with st.spinner('Flash busy, trying Pro...'):
                    response = model_pro.generate_content(prompt)
                    st.markdown("---")
                    st.markdown(response.text)
            except Exception as e2:
                st.error(f"Handshake Error: {e2}")
                st.info("Check Google AI Studio: Is the 'Generative Language API' enabled for your project?")
    else:
        st.warning("Please fill out all categories in the sidebar!")
