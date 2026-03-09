import streamlit as st
from google import genai
from google.genai import types

# 1. THE LOOK
st.set_page_config(page_title="Comedy Crowd Sim", page_icon="🎤", layout="centered")

st.markdown("""
<style>
    .main { background-color: #0e1117; color: #ffffff; }
    .stTextArea textarea { background-color: #161b22; color: #ffffff; border: 1px solid #30363d; }
    .crowd-response { background-color: #1f2937; border-left: 5px solid #facc15; padding: 20px; border-radius: 10px; margin-top: 20px; font-style: italic; }
</style>
""", unsafe_allow_html=True)

# 2. THE CONNECTION
try:
    api_key = st.secrets["api_key"]
    client = genai.Client(api_key=api_key)
except Exception:
    st.error("🔑 API Key Missing!")
    st.stop()

# 3. THE SETTINGS
with st.sidebar:
    st.title("🎟️ CLUB SETTINGS")
    crowd_type = st.selectbox("Crowd Type", ["Bachelorette Party", "Comedy Nerds", "Drunk Hecklers", "Corporate Retreat"])
    toughness = st.slider("Crowd Toughness", 1, 10, 5)
    lk = st.checkbox("Dry/Deadpan Mode")

# 4. THE STAGE
st.title("🎤 COMEDY CROWD SIM")
joke_input = st.text_area("Drop your bit or one-liner here:", height=200)

# 5. THE PERFORMANCE
if st.button("🎤 DELIVER JOKE"):
    if not joke_input:
        st.warning("Write a joke first!")
    else:
        with st.spinner("The crowd is leaning in..."):
            # BACK TO YOUR ORIGINAL CONFIG
            cfg = types.GenerateContentConfig(
                temperature=(0.1 if lk else 0.7), 
                top_p=0.95, 
                max_output_tokens=2000
            )
            
            # THE ONLY CHANGE: MARCH 9th STABLE NAMES
            m_list = ["gemini-3.1-flash", "gemini-2.5-flash", "gemini-2.0-flash-001"]
            
            p = f"React as a {crowd_type} (toughness {toughness}/10) to this joke: '{joke_input}'."

            success = False
            for model_name in m_list:
                try:
                    response = client.models.generate_content(
                        model=model_name,
                        contents=p,
                        config=cfg
                    )
                    st.session_state["crowd_feedback"] = response.text
                    success = True
                    break
                except Exception:
                    continue
            
            if success:
                st.rerun()
            else:
                st.error("The mic cut out!")

# 6. THE HECKLE
if "crowd_feedback" in st.session_state:
    st.markdown(f'<div class="crowd-response">{st.session_state["crowd_feedback"]}</div>', unsafe_allow_html=True)
    if st.button("Try a New Bit"):
        del st.session_state["crowd_feedback"]
        st.rerun()
