import streamlit as st
from google.genai import types
from google import genai

st.set_page_config(page_title="Comedy Simulator", page_icon="🎙️", layout="wide")

# 1. CSS - Navy & Yellow + Marquee Title + Sidebar Recovery
st.markdown("""<style>
    /* 1a. KILL THE BRANDING BUT SAVE THE SIDEBAR */
    #MainMenu {visibility: hidden !important;}
    footer {visibility: hidden !important;}
    header {visibility: hidden !important;}
    
    /* This targets the 'Crown/Avatar' toolbar specifically without shifting the page */
    .stAppToolbar {
        visibility: hidden !important;
        display: none !important;
    }
    
    /* Ensures the sidebar button stays visible and clickable */
    [data-testid="stSidebarNav"] {padding-top: 2rem;}
    
    /* 1b. YOUR ORIGINAL STYLING */
    .main-title { 
        color: #1e3a8a; font-weight: 800; text-align: center; 
        border: 3px solid #1e3a8a; padding: 20px; border-radius: 20px; 
        background-color: #f8fbff; margin-bottom: 30px;
    }
    .mic-container { display: flex; flex-direction: column; align-items: center; justify-content: center; line-height: 0.8; margin-right: 10px; }
    .mic-head { font-size: 24px; margin-bottom: -2px; }
    .mic-pole { background-color: #facc15; width: 3px; height: 12px; margin-bottom: -1px; }
    .mic-base { background-color: #facc15; width: 14px; height: 3px; border-radius: 2px; }
    .sidebar-header { display: flex; align-items: center; justify-content: center; margin-bottom: 20px; }
    .stButton button { background-color: #facc15 !important; color: #1e3a8a !important; border: 2px solid #1e3a8a !important; font-weight: bold !important; border-radius: 12px !important; }
    [data-testid="stSidebar"] { background-color: #1e3a8a; }
    [data-testid="stSidebar"] * { color: #fef08a !important; }
    [data-testid="stWidgetLabel"] svg {
        filter: invert(86%) sepia(87%) saturate(356%) hue-rotate(352deg) brightness(102%) contrast(104%) !important;
    }
    .response-card { background-color: #eff6ff; border-left: 8px solid #facc15; padding: 20px; border-radius: 10px; color: #1e3a8a; }
</style>""", unsafe_allow_html=True)

# 2. DATA
api_key = st.secrets.get("api_key")
if not api_key:
    st.error("Missing API Key!"); st.stop()
client = genai.Client(api_key=api_key)

VN = ["Underground Comedy", "The Comedy Shop", "Don't Tell Comedy", "College Bar", "Dive Bar", "Upscale Bar", "Comedy Showcase", "Open Mic", "Craft Brewery", "Theater", "Corporate Mixer", "Elk's Lodge", "Toastmasters", "Casino Resort"]
AU = ["Normal", "Hostile", "Drunk", "Passive", "Hopeful but Skeptical", "Jaded", "Friendly", "Easily Offended", "Other Comics Watching", "New to Live Comedy"]
AG = ["Gen Z", "Millennials", "Gen X", "Boomers"]

# 3. SIDEBAR
with st.sidebar:
    st.markdown("""<div class="sidebar-header"><div class="mic-container">
    <div class="mic-head">🎙️</div><div class="mic-pole"></div><div class="mic-base"></div>
    </div><h3 style="margin:0;">STUDIO CONTROLS</h3></div>""", unsafe_allow_html=True)
    st.success("✅ GUEST ACCESS ACTIVE")
    city = st.text_input("City", value="San Luis Obispo")
    st.caption("Enter a City to get the Local Vibe")
    st.subheader("Venue")
    sel_v = [v for v in VN if st.checkbox(v, key=f"v_{v}")]
    st.subheader("Crowd Vibe")
    v_score = st.slider("Tough <-> Loving", 1, 10, 5)
    st.subheader("Audience Type")
    sel_a = [a for a in AU if st.checkbox(a, key=f"a_{a}")]
    st.subheader("Age Range")
    sel_ag = [ag for ag in AG if st.checkbox(ag, key=f"ag_{ag}")]
    st.markdown("---")
    st.subheader("🛠️ Workshop Tools")
    lk = st.checkbox("Lock Structure", value=True, help="Forces analysis of logic.")
    ch = st.checkbox("Coach Mode", value=False, help="Veteran headliner feedback.")
    ex = st.checkbox("Extend Bit", value=False, help="Brainstorm 3 extra minutes.")
    rf = st.checkbox("Local Refs", value=False, help="Local landmarks/jokes.")
    st.markdown("---")
    if "last_res" in st.session_state:
        st.download_button("💾 DOWNLOAD SET", st.session_state["last_res"], "set.txt", use_container_width=True)
    else:
        st.button("💾 Save (Run First)", disabled=True, use_container_width=True)

# 4. MAIN UI
st.markdown("<h1 class='main-title'>🎙️ COMEDY CROWD SIMULATOR</h1>", unsafe_allow_html=True)
bit = st.text_area("Your Material:", height=300, placeholder="Enter your joke...")

# 5. RUN LOGIC
if st.button("🚀 RUN SIMULATION", use_container_width=True):
    if city and sel_v:
        v_map = {1:"Hostile", 2:"Tough", 3:"Skeptical", 4:"Stiff", 5:"Normal", 6:"Warm", 7:"Friendly", 8:"Loving", 9:"On Fire", 10:"Legendary"}
        fb = bit if bit.strip() != "" else "Suggest new premises."
        p = f"Act as the audience. Venue: {sel_v}. City: {city}. Audience: {sel_a}. Ages: {sel_ag}. Rules: {v_map[v_score]}. Bit: {fb}. Provide a detailed 2-paragraph audience reaction."
        if rf: p += f" LOCALIZATION: {city} refs."
        if ch: p += " COACHING: structural tips."
        if ex: p += " EXTENSION: 3 mins new material."
        
        cfg = types.GenerateContentConfig(temperature=(0.1 if lk else 0.7), max_output_tokens=2000)
        try:
            with st.spinner("Analyzing Room..."):
                res = client.models.generate_content(model="gemini-2.0-flash-001", contents=p, config=cfg)
                st.session_state["last_res"] = f"--- BIT ---\n{bit}\n\n--- FEEDBACK ---\n{res.text}"
                st.rerun()
        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.warning("Select City and Venue!")

# 6. DISPLAY
if "last_res" in st.session_state:
    display_text = st.session_state["last_res"].split("--- FEEDBACK ---")[-1]
    st.markdown(f"<div class='response-card'><h3>🎭 The Crowd Reacts:</h3>{display_text}</div>", unsafe_allow_html=True)
