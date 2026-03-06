import streamlit as st
from google import genai
from google.genai import types

st.set_page_config(page_title="Comedy Crowd Simulator", page_icon="🎤", layout="wide")

# 1. CSS
st.markdown("""<style>
.stApp h1 { text-align: center; }
[data-testid="stSidebarUserContent"] { display: flex; flex-direction: column; height: 100vh; }
.sidebar-footer { margin-top: auto; padding: 20px 0; border-top: 1px solid #ddd; }
div[data-baseweb="textarea"] textarea { font-size: 16px !important; }
.stButton button { height: 3.5em; border-radius: 10px; font-weight: bold; }
</style>""", unsafe_allow_html=True)

# 2. CLIENT & DATA
api_key = st.secrets.get("api_key")
if not api_key:
    st.error("Missing API Key!")
    st.stop()
client = genai.Client(api_key=api_key, http_options={'api_version': 'v1'})

VENUES = ["Underground Comedy", "The Comedy Shop", "Don't Tell", "The College Gig", "Dive Bar", "Upscale Bar", "Comedy Showcase", "Open Mic Night", "Local Craft Brewery", "Wine Bar", "Coffee Shop", "The Theater", "House Party", "Corporate Event", "Toastmasters", "Elk's Club", "Staff Meeting", "Opening for Big Name"]
AUDIENCES = ["Normal", "Hostile", "Distracted", "Drunk", "Passive", "New to Comedy", "Skeptical", "Jaded", "Friendly", "Easily Offended", "Chatty", "Other Comics"]
AGES = ["Gen Z", "Millennials", "Gen X", "Boomers"]

# 3. SIDEBAR
with st.sidebar:
    st.title("🎤 Studio Controls")
    st.success("✅ Guest Access Active")
    
    with st.container():
        st.subheader("Tools")
        lock_mode = st.checkbox("Lock Structure", value=True)
        coach_mode = st.checkbox("Coach Mode", value=False)
        extend_mode = st.checkbox("Extend Bit", value=False)
        local_ref_mode = st.checkbox("Local Refs", value=False)
        st.markdown("---")
        
        st.subheader("Room Setup")
        city = st.text_input("City", value="San Luis Obispo")
        st.caption("Enter a City for the Local Vibe") 
        
        st.header("1. Venue")
        sel_v = [v for v in VENUES if st.checkbox(v, key=f"v_{v}")]
        
        st.header("2. Crowd Vibe")
        v_score = st.slider("Tough <-> Loving", 1, 10, 5)
        
        st.header("3. Audience Type")
        sel_a = [a for a in AUDIENCES if st.checkbox(a, key=f"a_{a}")]
        
        st.header("4. Age Range")
        sel_ag = [ag for ag in AGES if st.checkbox(ag, key=f"ag_{ag}")]

    st.markdown('<div class="sidebar-footer">', unsafe_allow_html=True)
    if "last_res" in st.session_state:
        st.download_button("💾 Download",
