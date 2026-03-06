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
    /* Style for the 'Help Link' button */
    .stButton > button[kind="secondary"] {
        border: none;
        background: transparent;
        text-decoration: underline;
        color: #007bff;
        padding: 0;
        height: auto;
        font-size: 14px;
    }
    div[data-baseweb="textarea"] textarea { font-size: 16px !important; }
    .stButton button { height: 3.5em; border-radius: 10px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# ... [API Key and Client setup code] ...

# --- 3. THE SIDEBAR ---
with st.sidebar:
    st.title("🎤 Studio Controls")
    
    with st.container():
        st.subheader("Workshop Tools")
        lock_mode = st.checkbox("Lock Structure", value=True)
        coach_mode = st.checkbox("Coach Mode", value=False)
        extend_mode = st.checkbox("Extend Bit", value=False)
        local_ref_mode = st.checkbox("Local Refs", value=False)
        
        # LINK-STYLE HELP TOGGLE
        if st.button("🔗 Quick Start Guide"):
            st.info("""
            **Quick Start:**
            - **Set Room:** Pick City, Venue, Audience.
            - **Input:** Paste jokes in the main box.
            - **Brainstorm:** Box blank + **Coach Mode** for 5 premises.
            - **Run:** Hit 'Run Simulation'.
            - **Save:** Download at bottom.
            """)
        
        st.markdown("---")
        # ... [Rest of Sidebar: Room Setup, Venues, etc.] ...
