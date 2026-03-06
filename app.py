import streamlit as st
from google import genai
from google.genai import types

# --- 1. SETUP ---
st.set_page_config(page_title="Comedy Crowd Simulator", page_icon="🎤", layout="wide")

# --- CUSTOM CSS: Centering, Mobile Label, and Pinned Footer ---
st.markdown("""
    <style>
    /* 1. Center the Main Title */
    .stApp h1 { text-align: center; width: 100%; }
    
    /* 2. Mobile "Options" Label */
    @media (max-width: 991px) {
        [data-testid="stHeader"]::before {
            content: 'Options'; position: absolute; left: 50px; top: 15px;
            font-weight: bold; font-size: 16px; color: #31333F; 
        }
    }
    
    /* 3. Pinned Sidebar Layout */
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
    
    /* 4. Style for the Quick Start 'Link' button */
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

    /* 5. General UI fixes */
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
VENUES = [
    "Underground Comedy", "The Comedy Shop", "Don't Tell", 
    "The College Gig", "Dive Bar", "Upscale Bar", 
    "Comedy Showcase", "Open Mic Night", 
    "Local Craft Brewery", "Wine Bar", 
    "Coffee Shop / Bookstore", "The Theater", 
    "House Party", "Corporate / Charity Event",
    "Toastmasters", "Elk's Club", "Company Staff Bonding Meeting", 
    "Opening for a Big Name"
]
AUDIENCES = ["Normal", "Hostile/Heckling", "Distracted", "Drunk", "Passive", "New to Comedy", "Skeptical but Hopeful", "Jaded", "Friendly", "Silence for No Reason", "Easily Offended", "Chatty", "Other Comics Watching"]
AGES = ["Gen Z", "Millennials", "Gen X", "Boomers"]

# --- 3. THE SIDEBAR ---
with st.sidebar:
    st.title("🎤 Studio Controls")
    
    # Scrollable Settings Container
    with st.container():
        st.subheader("Workshop Tools")
        lock_mode = st.checkbox("Lock Structure", value=True)
        coach_mode = st.checkbox("Coach Mode", value=False)
        extend_mode = st.checkbox("Extend Bit", value=False)
        local_ref_mode = st.checkbox("Local Refs", value=False)
        
        # Link-style help toggle
        if st.button("🔗 Quick Start Guide", kind="secondary"):
            st.info("""
            **Quick Start:**
            - **Set Room:** Pick City, Venue, Audience.
            - **Input:** Paste jokes in the main box.
            - **Brainstorm:** Box blank + **Coach Mode** for 5 premises.
            - **Run:** Hit 'Run Simulation'.
            - **Save:** Download at the bottom of this menu!
            """)
        
        st.markdown("---")
        st.subheader("Room Setup")
        city = st.text_input("City (Required)", value="San Luis Obispo")
        st.caption("Enter a City for the Local Vibe") 
        
        st.header("1. The Venue (Required)")
        sel_venues = [v for v in VENUES if st.checkbox(v, key=f"v_{v}")]
        
        st.header("2. The Audience (Optional)")
        sel_audiences = [a for a in AUDIENCES if st.checkbox(a, key=f"a_{a}")]
        
        st.header("3. Age Range (Optional)")
        sel_ages = [ag for ag in AGES if st.checkbox(ag, key=f"ag_{ag}")]

    # Pinned Footer Container
    st.markdown('<div class="sidebar-footer">', unsafe_allow_html=True)
    st.subheader("Session Management")
    if "last_response" in st.session_state:
        session_text = f"CITY: {st.session_state.get('last_city')}\n"
        session_text += f"BIT:\n{st.session_state.get('last_bit')}\n\n"
        session_text += f"FEEDBACK:\n{st.session_state['last_response']}"
        
        st.download_button("💾 Download This Session", data=session_text, file_name="comedy_set_feedback.txt", use_container_width=True)
    else:
        st.button("💾 Save (Run Simulation First)", disabled=True, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# --- 4. MAIN INTERFACE ---
st.title("🎤 Comedy Crowd Simulator")
bit_text = st.text_area("Paste your set here:",
