import streamlit as st
from google import genai
from google.genai import types

st.set_page_config(page_title="Comedy Crowd Simulator", page_icon="🎙️", layout="wide")

# 1. CSS - Navy & Yellow + NEW BORDERED TITLE
st.markdown("""<style>
    .main-title { 
        color: #1e3a8a; 
        font-weight: 800; 
        text-align: center; 
        border: 3px solid #1e3a8a; 
        padding: 20px; 
        border-radius: 20px; 
        background-color: #f8fbff;
        margin-bottom: 25px;
    }
    .mic-container { display: flex; flex-direction: column; align-items: center; justify-content: center; line-height: 0.8; margin-right: 10px; }
    .mic-head { font-size: 24px; margin-bottom: -2px; }
    .mic-pole { background-color: #facc15; width: 3px; height: 12px; margin-bottom: -1px; }
    .mic-base { background-color: #facc15; width: 14px; height: 3px; border-radius: 2px; }
    .sidebar-header { display: flex; align-items: center; justify-content: center; margin-bottom: 20px; }
    .stButton button { background-color: #facc15 !important; color: #1e3a8a !important; border: 2px solid #1e3a8a !important; font-weight: bold !important; border-radius: 12px !important; }
    [data-testid="stSidebar"] { background-color: #1e3a8a; }
    [data-testid="stSidebar"] * { color: #fef08a !important; }
    
    /* THE YELLOW TOOLTIP FILTER */
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

VENUES = ["Underground", "The Comedy Shop", "Don't Tell", "College Gig", "Dive Bar", "Upscale Bar", "Showcase", "Open Mic", "Brewery", "Theater", "House Party", "Corporate"]
AUDIENCES = ["Normal", "Hostile", "Distracted", "Drunk", "Passive", "Skeptical", "Jaded", "Friendly", "Easily Offended", "Other Comics"]
AGES = ["Gen Z", "Millennials", "Gen X", "Boomers"]

# 3. SIDEBAR
with st.sidebar:
    st.markdown("""<div class="sidebar-header"><div class="mic-container">
    <div class="mic-head">🎙️</div><div class="mic-pole"></div><div class="mic-base"></div>
    </div><h3 style="margin:0;">STUDIO CONTROLS</h3></div>""", unsafe_allow_html=True)
    st.success("✅ GUEST ACCESS ACTIVE")
    st.subheader("🛠️ Workshop Tools")
    
    lk = st.checkbox("Lock Structure", value=True, help="Keeps AI on joke logic.")
    ch = st.checkbox("Coach Mode", value=False, help="Adds structural feedback.")
    ex = st.checkbox("Extend Bit", value=False, help="Brainstorms next 3 mins.")
    rf = st.checkbox("Local Refs", value=False, help="Includes city landmarks.")
    
    st.markdown("---")
    city = st.text_input("City", value="San Luis Obispo")
    st.caption("Enter a City to get the Local Vibe")
    
    sel_v = [v for v in VENUES if st.checkbox(v, key=f"v_{v}")]
    v_score = st.slider("Tough <-> Loving", 1, 10, 5)
    sel_a = [a for a in AUDIENCES if st.checkbox(a, key=f"a_{a}")]
    sel_ag = [ag for ag in AGES if st.checkbox(ag, key=f"ag_{ag}")]
    
    st.markdown("---")
    if "last_res" in st.session_state:
        st.download_button("💾 DOWNLOAD SET", st.session_state["last_res"], "set.txt", use_container_width=True)
    else:
        st.button("💾 Save (Run First)", disabled=True, use_container_width=True)

# 4. MAIN UI
st.markdown("<h1 class='main-title'>🎙️ COMEDY CROWD SIMULATOR</h1>", unsafe_allow_html=True)

bit = st.text_area("Your Material:", height=300, 
    placeholder="Enter your joke or bit here to see how it might land with your crowd... Or check Coach and leave blank for suggestions.")

# 5. RUN LOGIC
if st.button("🚀 RUN SIMULATION", use_container_width=True):
    if city and sel_v:
        fb = bit if bit.strip() != "" else "Suggest new premises."
        cfg = types.GenerateContentConfig(temperature=(0.1 if lk else 0.7), top_p=0.95, max_output_tokens=2000)
        v_map = {1:"Hostile", 2:"Tough", 3:"Skeptical", 4:"Stiff", 5:"Normal", 6:"Warm", 7:"Friendly", 8:"Loving", 9:"On Fire", 10:"Legendary"}
        p = f"Act as audience. Venue: {sel_v}. City: {city}. Ages: {sel_ag}. Rules: {v_map[v_score]}. Bit: {fb}"
        
        m_list = ["gemini-3-flash-preview", "gemini-1.5-flash"]
        for m_name in m_list:
            try:
                with st.spinner(f"Testing {m_name}..."):
                    res = client.models.generate_content(model=m_name, contents=p, config=cfg)
                    st.session_state["last_res"] = res.text
                    st.rerun()
            except Exception as e:
                if "503" in str(e) and m_name != m_list[-1]: continue
                st.error(f"Error: {e}"); break
    else:
        st.warning("Select City and Venue!")

# 6. DISPLAY
if "last_res" in st.session_state:
    out_txt = st.session_state["last_res"]
    st.markdown(f"""
        <div class='response-card'>
            <h3>🎭 The Crowd Reacts:</h3>
            {out_txt}
        </div>
    """, unsafe_allow_html=True)
