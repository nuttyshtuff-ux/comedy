import streamlit as st
from google import genai
from google.genai import types

# --- 1. SETUP ---
st.set_page_config(page_title="Comedy Crowd Simulator", page_icon="🎤", layout="wide")

# --- CUSTOM CSS: Centering & Mobile Label ---
st.markdown("""
    <style>
    /* 1. Center the Main Title */
    .stApp h1 {
        text-align: center;
        width: 100%;
    }

    /* 2. Add "Options" label next to the hamburger menu on mobile */
    [data-testid="stHeader"]::before {
        content: 'Options';
        position: absolute;
        left: 50px;
        top: 15px;
        font-weight: bold;
        font-size: 16px;
        color: #31333F; 
    }

    /* 3. Mobile font fix & Button styling */
    div[data-baseweb="textarea"] textarea { font-size: 16px !important; }
    .stButton button {
        height: 3.5em;
        border-radius: 10px;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

api_key = st.secrets.get("api_key")
if not api_key:
    st.error("Missing API Key!")
    st.stop()

client = genai.Client(api_key=api_key, http_options={'api_version': 'v1'})

# --- 2. DATA ---
VENUES = ["Underground Comedy", "The Comedy Shop", "Don't Tell", "The College Gig", "Dive Bar", "Upscale Bar", "Comedy Showcase", "Open Mic Night", "Local Craft Brewery", "Wine Bar", "Coffee Shop / Bookstore", "The Theater", "House Party", "Corporate / Charity Event", "Opening for a Big Name"]
AUDIENCES = ["Normal", "Hostile/Heckling", "Distracted", "Drunk", "Passive", "New to Comedy", "Skeptical but Hopeful", "Jaded", "Friendly", "Silence for No Reason", "Easily Offended", "Chatty", "Other Comics Watching"]
AGES = ["Gen Z", "Millennials", "Gen X", "Boomers"]

# --- 3. THE SIDEBAR ---
with st.sidebar:
    st.title("🎤 Studio Controls")
    
    st.subheader("Workshop Tools")
    lock_mode = st.checkbox("Lock Structure", value=True, help="✅ Checked: Precise feedback. ❌ Unchecked: Creative variations.")
    coach_mode = st.checkbox("Coach Mode", value=False, help="Critique a joke or (if blank) get premises.")
    extend_mode = st.checkbox("Extend Bit", value=False, help="Suggest ways to keep the joke going.")
    local_ref_mode = st.checkbox("Local Refs", value=False, help="Inject landmarks and inside jokes for the city.")
    
    st.markdown("---")
    st.subheader("Room Setup")
    city = st.text_input("City (Required)", value="San Luis Obispo")
    
    st.header("1. The Venue (Required)")
    sel_venues = [v for v in VENUES if st.checkbox(v, key=f"v_{v}")]
    
    st.header("2. The Audience (Optional)")
    sel_audiences = [a for a in AUDIENCES if st.checkbox(a, key=f"a_{a}")]
    
    st.header("3. Age Range (Optional)")
    sel_ages = [ag for ag in AGES if st.checkbox(ag, key=f"ag_{ag}")]
    
    if "last_response" in st.session_state:
        st.markdown("---")
        session_text = f"CITY: {st.session_state.get('last_city')}\n\nBIT:\n{st.session_state.get('last_bit')}\n\nFEEDBACK:\n{st.session_state['last_response']}"
        st.download_button("💾 Download Session", data=session_text, file_name="comedy_session.txt", use_container_width=True)

# --- 4. MAIN INTERFACE ---
st.title("🎤 Comedy Crowd Simulator")

bit_text = st.text_area("Paste your set here:", height=300, placeholder="Type your bit here...")

# --- 5. EXECUTION ---
if st.button("🚀 Run Simulation / Generate Prompts", use_container_width=True):
    if city.strip() and sel_venues:
        try:
            current_temp = 0.1 if
