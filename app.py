import streamlit as st
from google import genai
from google.genai import types

# --- 1. SETUP ---
st.set_page_config(page_title="Comedy Crowd Sim", page_icon="🎤", layout="wide")

api_key = st.secrets.get("api_key")
if not api_key:
    st.error("Missing API Key!")
    st.stop()

client = genai.Client(api_key=api_key, http_options={'api_version': 'v1'})

# --- 2. DATA ---
VENUES = ["Underground Comedy", "The Comedy Shop", "Don't Tell", "The College Gig", "Dive Bar", "Upscale Bar", "Comedy Showcase", "Open Mic Night", "Local Craft Brewery", "Wine Bar", "Coffee Shop / Bookstore", "The Theater", "House Party", "Corporate / Charity Event", "Opening for a Big Name"]
AUDIENCES = ["Normal", "Hostile/Heckling", "Distracted", "Drunk", "Passive", "New to Comedy", "Skeptical but Hopeful", "Jaded", "Friendly", "Silence for No Reason", "Easily Offended", "Chatty", "Other Comics Watching"]
AGES = ["Gen Z", "Millennials", "Gen X", "Boomers"]

# --- 3. THE SIDEBAR (All Controls Live Here Now) ---
with st.sidebar:
    st.title("🎤 Studio Controls")
    
    # NEW: Mode Toggles moved here for Mobile usability
    st.subheader("Workshop Tools")
    lock_mode = st.checkbox("Lock Structure", value=True, help="Reliable format vs Creative wildcard.")
    coach_mode = st.checkbox("Coach Mode", value=False, help="Critique or (if blank) get premises.")
    extend_mode = st.checkbox("Extend Bit", value=False, help="Suggest ways to keep the joke going.")
    local_ref_mode = st.checkbox("Local Refs", value=False, help="Inject city-specific landmarks.")
    
    st.markdown("---")
    
    # Room Setup
    st.subheader("Room Setup")
    city = st.text_input("City (Required)", value="San Luis Obispo")
    
    st.header("1. The Venue (Required)")
    sel_venues = [v for v in VENUES if st.checkbox(v, key=f"v_{v}")]
    
    st.header("2. The Audience (Optional)")
    sel_audiences = [a for a in AUDIENCES if st.checkbox(a, key=f"a_{a}")]
    
    st.header("3. Age Range (Optional)")
    sel_ages = [ag for ag in AGES if st.checkbox(ag, key=f"ag_{ag}")]
    
    st.markdown("---")
    # Download button moved to sidebar bottom
    if "last_response" in st.session_state:
        session_text = f"CITY: {st.session_state.get('last_city')}\n\nBIT:\n{st.session_state.get('last_bit')}\n\nFEEDBACK:\n{st.session_state['last_response']}"
        st.download_button("💾 Download Session", data=session_text, file_name="comedy_session.txt", use_container_width=True)

# --- 4. MAIN INTERFACE ---
st.title("🎤 Comedy Crowd Sim")

# Mobile CSS Tweak: Ensures text area and buttons are easy to tap
st.markdown("""
    <style>
    div[data-baseweb="textarea"] textarea { font-size: 16px !important; }
    .stButton button { height: 3.5em; border-radius: 10px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

bit_text = st.text_area("Paste your set here:", height=300, placeholder="Type your bit here...")

# --- 5. EXECUTION ---
if st.button("🚀 Run Simulation / Generate Prompts", use_container_width=True):
    if city.strip() and sel_venues:
        try:
            current_temp = 0.1 if lock_mode else 0.7
            config = types.GenerateContentConfig(temperature=current_temp, top_p=0.95, max_output_tokens=3000)

            instructions = []
            if coach_mode: instructions.append("- Provide a 'COACH'S CORNER' feedback section.")
            if extend_mode: instructions.append("- Provide 'THE NEXT 3 MINUTES' with expansion ideas.")
            if local_ref_mode: instructions.append(f"- Provide 5 specific local references for {city}.")
            
            instr_str = "\n".join(instructions)
            venue_str = ", ".join(sel_venues)
            aud_str = ", ".join(sel_audiences) if sel_audiences else "Mixed"
            age_str = ", ".join(sel_ages) if sel_ages else "All Ages"

            if not bit_text.strip():
                prompt = f"ACT AS A COMEDY WRITING PARTNER. You MUST provide EXACTLY 5 distinct comedy premises for {city} at {venue_str}. Audience: {aud_str} | Age: {age_str}. {instr_str}\nSTRUCTURE: 1. PREMISE 1, 2. PREMISE 2, 3. PREMISE 3, 4. PREMISE 5, 6. ADDITIONAL SECTIONS."
            else:
                prompt = f"ACT AS A COMEDY AUDIENCE SIMULATOR. Simulate this bit: '{bit_text}' for {city} | {venue_str} | {aud_str} | {age_str}. {instr_str}"

            with st.spinner("Processing..."):
                response = client.models.generate_content(model="gemini-2.5-flash", contents=prompt, config=config)
                st.session_state['last_response'] = response.text
                st.session_state['last_city'] = city
                st.session_state['last_bit'] = bit_text if bit_text.strip() else "Brainstorming Session"
                st.rerun()
                
        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.warning("Please select City and Venue in the sidebar!")

# --- 6. DISPLAY ---
if "last_response" in st.session_state:
    st.markdown("---")
    st.markdown(st.session_state['last_response'])
    if "100%" in st.session_state['last_response']:
        st.balloons()
