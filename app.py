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
CROWD_PRESETS = {
    "The College Gig": {"size": 25, "age": "Gen Z", "vibe": "Encouraging but Naive", "desc": "TikTok attention spans."},
    "The Biker Bar": {"size": 40, "age": "Gen X", "vibe": "Drunk/Rowdy", "desc": "Leather and zero patience."},
    "The VFW Hall": {"size": 30, "age": "Boomer", "vibe": "Corporate/Cold", "desc": "Staring at you over a pitcher of light beer."},
    "The Tech Mixer": {"size": 60, "age": "Millennial", "vibe": "Corporate/Cold", "desc": "Everyone is checking their Slack notifications."},
    "The 'Last Resort'": {"size": 5, "age": "Mixed", "vibe": "Drunk/Rowdy", "desc": "Just three guys and a bartender who hates you."},
    "The Woke Workshop": {"size": 20, "age": "Gen Z", "vibe": "Encouraging but Naive", "desc": "Waiting for you to say something problematic."},
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
    
    with st.sidebar:
    st.header("Step 1: The Crowd Base")
    base_room = st.selectbox("Base Crowd", list(CROWD_PRESETS.keys()))
    
    st.header("Step 2: The Modifier")
    # This adds the 'Combination' element
    modifier = st.selectbox("Current State", [
        "Normal", 
        "Hostile/Heckling", 
        "Distracted by Sports on TV", 
        "High/Edibles Kicking In", 
        "Actually Liking You"
    ])

    # Dynamic Description Logic
    room = CROWD_PRESETS[base_room]
    final_desc = f"{room['desc']} + {modifier} Mode"
    
    st.success(f"Targeting: {final_desc}")

bit_text = st.text_area("Paste your bit here:", placeholder="I've always been a grumpy old man...", height=200)

if st.button("Do the Bit"):
    if bit_text:
        model = genai.GenerativeModel('gemini-1.5-flash')
        full_query = f"""
SCENARIO: You are simulating a comedy club crowd.
BASE CROWD: {base_room} ({room['age']}, {room['vibe']})
MODIFIER: {modifier}
CONTEXT: {room['desc']}

BIT TO EVALUATE: 
{bit_text}

AI TASK: Respond as if the modifier is fighting the base crowd. 
(e.g., If it's a VFW Hall + Edibles, the Boomers are staring but slowly starting to giggle at the glow-in-the-dark Jesus.)
"""
        
        with st.spinner('Waiting for the room to react...'):
            response = model.generate_content([SYSTEM_PROMPT, full_query])
            st.markdown("---")
            st.markdown(response.text)
    else:

        st.warning("You gotta say something first, Grampa!")



