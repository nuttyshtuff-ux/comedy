import streamlit as st
import google.generativeai as genai

CROWD_PRESETS = {
    "The College Gig": {
        "size": 25,
        "age": "Gen Z",
        "vibe": "Encouraging but Naive",
        "desc": "12-year-olds with TikTok brain."
    },
    "The Biker Bar": {
        "size": 40,
        "age": "Gen X",
        "vibe": "Drunk/Rowdy",
        "desc": "Leather jackets and zero patience."
    },
    "The Corporate Breakfast": {
        "size": 100,
        "age": "Millennial",
        "vibe": "Corporate/Cold",
        "desc": "8 AM, no coffee, looking for a reason to HR you."
    },
    "The Open Mic Night": {
        "size": 15,
        "age": "Mixed",
        "vibe": "Open Mic Comics",
        "desc": "Just 10 guys waiting for their turn to talk."
    }
}
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
    st.header("Step 1: Pick Your Room")
    
    # Select a preset
    preset_name = st.selectbox("Choose a Preset", list(CROWD_PRESETS.keys()))
    room = CROWD_PRESETS[preset_name]
    
    st.info(f"Current Vibe: {room['desc']}")
    
    st.divider()
    st.header("Fine-Tune Settings")
    
    # Use the preset values as 'defaults' for the sliders/selects
    size = st.slider("Crowd Size", 5, 500, room['size'])
    age = st.selectbox("Age Group", ["Gen Z", "Millennial", "Gen X", "Boomer", "Mixed"], 
                       index=["Gen Z", "Millennial", "Gen X", "Boomer", "Mixed"].index(room['age']))
    vibe = st.selectbox("Room Vibe", ["Encouraging but Naive", "Drunk/Rowdy", "Corporate/Cold", "Open Mic Comics"],
                        index=["Encouraging but Naive", "Drunk/Rowdy", "Corporate/Cold", "Open Mic Comics"].index(room['vibe']))

bit_text = st.text_area("Paste your bit here:", placeholder="I've always been a grumpy old man...", height=200)

if st.button("Do the Bit"):
    if bit_text:
        model = genai.GenerativeModel('gemini-1.5-flash')
        full_query = f"""
Analyze this set for: {preset_name}.
Details: {size} people, mostly {age}, feeling {vibe}.
The specific room description is: {room['desc']}
Bit: {bit_text}
"""
        
        with st.spinner('Waiting for the room to react...'):
            response = model.generate_content([SYSTEM_PROMPT, full_query])
            st.markdown("---")
            st.markdown(response.text)
    else:

        st.warning("You gotta say something first, Grampa!")


