import streamlit as st
from google import genai
from google.genai import types

# --- 1. SETUP ---
st.set_page_config(page_title="Comedy Crowd Simulator", page_icon="🎤", layout="wide")

# --- CUSTOM CSS ---
st.markdown("""
    <style>
    .stApp h1 { text-align: center; width: 100%; }
    @media (max-width: 991px) {
        [data-testid="stHeader"]::before {
            content: 'Options'; position: absolute; left: 50px; top: 15px;
            font-weight: bold; font-size: 16px; color: #31333F; 
        }
    }
    [data-testid="stSidebarUserContent"] {
        display: flex;
        flex-direction: column;
        height: 100vh;
    }
    .sidebar-footer {
        margin-top: auto;
        padding-top: 20px;
        padding-bottom: 20px;
        border-top: 1px solid #ddd;
    }
    .stButton > button[kind="secondary"] {
        border: none;
        background: transparent;
        text-decoration: underline;
        color: #007bff;
        padding: 0;
        height: auto;
        font-size: 14px;
        text-align: left;
    }
    div[data-baseweb="textarea"] textarea { font-size: 16px !important; }
    .stButton button { height: 3.5em; border-radius: 10px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# API KEY CHECK
api_key = st.secrets.get("api_key")
if not api_key:
    st.error("Missing API Key in Secrets!")
    st.stop()

client = genai.Client(api_key=api_key, http_options={'api_version': 'v1'})

# --- 2. DATA ---
VENUES = ["Underground Comedy", "The Comedy Shop", "Don't Tell", "The College Gig", "Dive Bar", "Upscale Bar", "Comedy Showcase", "Open Mic Night", "Local Craft Brewery", "Wine Bar", "Coffee Shop / Bookstore", "The Theater", "House Party", "Corporate / Charity Event", "Toastmasters", "Elk's Club", "Company Staff Bonding Meeting", "Opening for a Big Name"]
AUDIENCES = ["Normal", "Hostile/Heckling", "Distracted", "Drunk", "Passive", "New to Comedy", "Skeptical but Hopeful", "Jaded", "Friendly", "Silence for No Reason", "Easily Offended", "Chatty", "Other Comics Watching"]
AGES = ["Gen Z", "Millennials", "Gen X", "Boomers"]

# --- 3. THE SIDEBAR ---
with st.sidebar:
    st.title("🎤 Studio Controls")
    
    with st.container():
        st.subheader("Workshop Tools")
        lock_mode = st.checkbox("Lock Structure", value=True)
        coach_mode = st.checkbox("Coach Mode", value=False)
        extend_mode = st.checkbox("Extend Bit", value=False)
        local_ref_mode = st.checkbox("Local Refs", value=False)
        
        if st.button("🔗 Quick Start Guide", kind="secondary"):
            st.info("Pick your Venue, paste your set, and hit Run. Use Coach Mode for premises!")
        
        st.markdown("---")
        st.subheader("Room Setup")
        city = st.text_input("City (Required)", value="San Luis Obispo")
        st.caption("Enter a City for the Local Vibe") 
        
        st.header("1. Venue (Required)")
        sel_venues = [v for v in VENUES if st.checkbox(v, key=f"v_{v}")]
        
        st.header("2. Audience")
        sel_audiences = [a for a in AUDIENCES if st.checkbox(a, key=f"a_{a}")]
        
        st.header("3. Age Range")
        sel_ages = [ag for ag in AGES if st.checkbox(ag, key=f"ag_{ag}")]

    # FOOTER
    st.markdown('<div class="sidebar-footer">', unsafe_allow_html=True)
    st.subheader("Session Management")
    if "last_response" in st.session_state:
        st.download_button("💾 Download", data=st.session_state.get('last_response'), file_name="feedback.txt", use_container_width=True)
    else:
        st.button("💾 Save (Run First)", disabled=True, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# --- 4. MAIN INTERFACE ---
st.title("🎤 Comedy Crowd Simulator")
bit_text = st.text_area("Paste your set here:", height=300, placeholder="Type your bit here...")

# --- 5. EXECUTION ---
if st.button("🚀 Run Simulation / Generate Prompts", use_container_width=True):
    if city.strip() and sel_venues:
        try:
            current_temp = 0.1 if lock_mode else 0.7
            config = types.GenerateContentConfig(temperature=current_temp, top_p=0.95, max_output_tokens=3000)

            # --- BUILD PROMPT INSTRUCTIONS ---
            instr = []
            if coach_mode: instr.append("- Provide a 'COACH'S CORNER' feedback section.")
            if extend_mode: instr.append("- Provide 'THE NEXT 3 MINUTES' with expansion ideas.")
            if local_ref_mode: 
                ref_text = f"- Provide 5 local references for {city
