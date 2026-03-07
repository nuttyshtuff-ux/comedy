import streamlit as st
from google import genai
from google.genai import types

# 1. PAGE CONFIG
st.set_page_config(page_title="Comedy Crowd Simulator", page_icon="🎤", layout="wide")

# 2. TARGETED COLOR INJECTION (Clean & High Contrast)
st.markdown("""
<style>
    /* Main Title & Accents */
    .main-title {
        color: #1e3a8a; /* Deep Navy Blue */
        font-weight: 800;
        text-align: center;
        margin-bottom: 0px;
    }
    .mic-icon { color: #facc15; font-size: 50px; text-align: center; } /* Bright Yellow */
    
    /* The Run Button - Electric Yellow */
    .stButton button {
        background-color: #facc15 !important;
        color: #1e3a8a !important;
        border: 2px solid #1e3a8a !important;
        font-weight: bold !important;
        font-size: 20px !important;
        border-radius: 12px !important;
        transition: 0.3s all ease;
    }
    .stButton button:hover {
        background-color: #1e3a8a !important;
        color: #facc15 !important;
        transform: translateY(-2px);
    }

    /* Sidebar - Professional Navy */
    [data-testid="stSidebar"] {
        background-color: #1e3a8a;
        color: white;
    }
    [data-testid="stSidebar"] .stMarkdown, [data-testid="stSidebar"] p, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
        color: #fef08a !important; /* Soft Yellow text for sidebar headers */
    }

    /* Response Box - Soft Blue Wash */
    .response-card {
        background-color: #eff6ff;
        border-left: 8px solid #facc15;
        padding: 25px;
        border-radius: 10px;
        color: #1e3a8a;
    }
</style>
""", unsafe_allow_html=True)

# 2. CLIENT & DATA
api_key = st.secrets.get("api_key")
if not api_key:
    st.error("Missing API Key!")
    st.stop()
client = genai.Client(api_key=api_key)

VENUES = ["Underground Comedy", "The Comedy Shop", "Don't Tell", "The College Gig", "Dive Bar", "Upscale Bar", "Comedy Showcase", "Open Mic Night", "Local Craft Brewery", "Wine Bar", "Coffee Shop", "The Theater", "House Party", "Corporate Event", "Toastmasters", "Elk's Club", "Staff Meeting", "Opening for Big Name"]
AUDIENCES = ["Normal", "Hostile", "Distracted", "Drunk", "Passive", "New to Comedy", "Skeptical", "Jaded", "Friendly", "Easily Offended", "Chatty", "Other Comics"]
AGES = ["Gen Z", "Millennials", "Gen X", "Boomers"]

# 3. SIDEBAR
with st.sidebar:
    st.markdown("<div class='mic-icon'>🎤</div>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center;'>STUDIO</h2>", unsafe_allow_html=True)
    st.success("✅ GUEST ACCESS ACTIVE")
    
    with st.container():
        st.subheader("🛠️ Tools")
        lock_mode = st.checkbox("Lock Structure", value=True, help="Keep logic tight.")
        coach_mode = st.checkbox("Coach Mode", value=False, help="Technical feedback.")
        extend_mode = st.checkbox("Extend Bit", value=False, help="Generate next 3 mins.")
        local_ref_mode = st.checkbox("Local Refs", value=False, help="Use city landmarks.")
        
        st.markdown("---")
        city = st.text_input("Current City", value="San Luis Obispo")
        
        st.header("1. Venue")
        sel_v = [v for v in VENUES if st.checkbox(v, key=f"v_{v}")]
        st.header("2. Crowd Vibe")
        v_score = st.slider("Tough <-> Loving", 1, 10, 5)
        st.header("3. Audience Type")
        sel_a = [a for a in AUDIENCES if st.checkbox(a, key=f"a_{a}")]
        st.header("4. Age Range")
        sel_ag = [ag for ag in AGES if st.checkbox(ag, key=f"ag_{ag}")]

    # Footer
    st.markdown("---")
    if "last_res" in st.session_state:
        st.download_button("💾 Download Set", data=st.session_state["last_res"], file_name="set.txt", use_container_width=True)
    
    donate_url = "https://www.paypal.com/paypalme/mrcoward"
    st.markdown(f'''<a href="{donate_url}" target="_blank" style="text-decoration: none;">
            <div style="background-color: #facc15; color: #1e3a8a; text-align: center; padding: 10px; border-radius: 8px; font-weight: bold;">
                ☕ Buy the Dev a Coffee
            </div></a>''', unsafe_allow_html=True)

# 4. MAIN UI
st.markdown("<h1 class='main-title'>🎤 COMEDY CROWD SIMULATOR</h1>", unsafe_allow_html=True)
st.write("---")

bit = st.text_area(
    "Your Material:", 
    height=300, 
    placeholder="Enter your jokes or bit here to see how your crowd will react..."
)

# 5. RUN LOGIC
if st.button("🚀 RUN SIMULATION", use_container_width=True):
    if city and sel_v:
        models = ["gemini-3
