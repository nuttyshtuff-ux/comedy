import streamlit as st
import google.generativeai as genai
st.set_page_config(
    page_title="Comedy Crowd Sim",
    page_icon="🎤",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- 1. SETUP ---
st.set_page_config(page_title="Comedy Crowd Sim", page_icon="🎤")

# PASTE YOUR KEY INSIDE THE QUOTES BELOW
api_key = "YOUR_API_KEY_HERE" 
genai.configure(api_key=api_key)

# --- 2. THE PROMPT ENGINE ---
SYSTEM_PROMPT = """
You are a Professional Comedy Simulation Engine. 
The user will provide crowd stats and a comedy bit.
Your response MUST include:
1. ROOM SOUND: (e.g., *Scattered chuckles*, *Dead silence*)
2. PERSONA FEEDBACK: 3 specific reactions from different audience members.
3. THE SCORECARD: Laughter Meter (0-100%), Relatability, and 'Oof' Factor.
4. COACH'S TIP: One sentence on how to improve the bit for THIS specific crowd.
"""

# --- 3. THE USER INTERFACE ---
st.title("🎤 The Crowd Evaluator")
st.markdown("### *Test your set before the robots take over.*")

with st.sidebar:
    st.header("The Room")
    size = st.slider("Crowd Size", 5, 500, 25)
    vibe = st.selectbox("Room Vibe", ["Encouraging but Naive", "Drunk/Rowdy", "Corporate/Cold", "Open Mic Comics"])
    age = st.select_slider("Main Age Group", options=["Gen Z", "Millennial", "Gen X", "Boomer"])

bit_text = st.text_area("Paste your bit here:", placeholder="I've always been a grumpy old man...", height=200)

if st.button("Do the Bit"):
    if bit_text:
        model = genai.GenerativeModel('gemini-1.5-flash')
        full_query = f"Crowd: {size} people, {age}, Vibe: {vibe}.\nBit: {bit_text}"
        
        with st.spinner('Waiting for the room to react...'):
            response = model.generate_content([SYSTEM_PROMPT, full_query])
            st.markdown("---")
            st.markdown(response.text)
    else:

        st.warning("You gotta say something first, Grampa!")

