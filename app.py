import streamlit as st
import google.generativeai as genai

CROWD_PRESETS = {
    "The College Gig": {"size": 25, "age": "Gen Z", "vibe": "Encouraging but Naive", "desc": "TikTok attention spans."},
    "The Biker Bar": {"size": 40, "age": "Gen X", "vibe": "Drunk/Rowdy", "desc": "Leather and zero patience."},
    "The VFW Hall": {"size": 30, "age": "Boomer", "vibe": "Corporate/Cold", "desc": "Staring over light beer."},
    "The Tech Mixer": {"size": 60, "age": "Millennial", "vibe": "Corporate/Cold", "desc": "Checking Slack notifications."},
    "The 'Last Resort'": {"size": 5, "age": "Mixed", "vibe": "Drunk/Rowdy", "desc": "Three guys and a mean bartender."},
    "The Woke Workshop": {"size": 20, "age": "Gen Z", "vibe": "Encouraging but Naive", "desc": "Waiting for a 'problematic' slip-up."},
    "The Open Mic Night": {"size": 15, "age": "Mixed", "vibe": "Open Mic Comics", "desc": "Just comics waiting for their turn."}
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
Your goal is to provide a 'Deep Dive' analysis of a stand-up comedy bit.

EVALUATION PARAMETERS:
1. THE ROOM SOUND: Literal auditory feedback (e.g., *Tense silence*, *A single loud snort*, *Roaring laughter*).
2. AUDIENCE PERSONAS: Give 3 distinct reactions (e.g., 'The Skeptic', 'The Easy Laugh', 'The Heckler').
3. TECHNICAL BREAKDOWN: 
   - Setup/Punchline Efficiency: Is the word count too high?
   - Originality: Is this a 'hack' premise or a fresh take?
   - Vibe Check: Did the bit match the chosen crowd's specific 'Modifier'?
4. THE SCORECARD: Laughter (0-100%), Tension Level, and 'Kill' Probability.
5. COACH'S TIP: One actionable sentence to make the punchline hit harder.
"""

# --- 3. THE USER INTERFACE ---
st.title("🎤 The Crowd Evaluator")
st.markdown("### *Test your set before the robots take over.*")

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
st.divider()
    st.header("Step 3: Performance Style")
    style = st.selectbox("Style", [
        "Observational", 
        "Deadpan/One-Liners", 
        "Storytelling", 
        "Self-Deprecating", 
        "High Energy/Physical"
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








