import streamlit as st
from google import genai
from google.genai import types

st.set_page_config(page_title="Comedy Crowd Simulator", page_icon="🎤", layout="wide")

# 1. CSS - Navy & Yellow High-Contrast Theme
st.markdown("""<style>
    .main-title { color: #1e3a8a; font-weight: 800; text-align: center; }
    .mic-icon { color: #facc15; font-size: 50px; text-align: center; margin-bottom: 10px; }
    .stButton button {
        background-color: #facc15 !important; color: #1e3a8a !important;
        border: 2px solid #1e3a8a !important; font-weight: bold !important;
        font-size: 20px !important; border-radius: 12px !important;
    }
    [data-testid="stSidebar"] { background-color: #1e3a8a; }
    [data-testid="stSidebar"] * { color: #fef08a !important; }
    .response-card {
        background-color: #eff6ff; border-left: 8px solid #facc15;
        padding: 20px; border-radius: 10px; color: #1e3a8a;
    }
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
    st.markdown("<div class='mic-icon'>🎤</div>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center;'>STUDIO CONTROLS</h3>", unsafe_allow_html=True)
    st.success("✅ GUEST ACCESS ACTIVE")
    
    st.subheader("🛠️ Workshop Tools")
    lock_mode = st.checkbox("Lock Structure", value=True)
    coach_mode = st.checkbox("Coach Mode", value=False)
    extend_mode = st.checkbox("Extend Bit", value=False)
    local_ref_mode = st.checkbox("Local Refs", value=False)
    
    st.markdown("---")
    city = st.text_input("City", value="San Luis Obispo")
    
    st.header("1. Venue")
    sel_v = [v for v in VENUES if st.checkbox(v, key=f"v_{v}")]
    
    st.header("2. Crowd Vibe")
    v_score = st.slider("Tough <-> Loving", 1, 10, 5)
    
    st.header("3. Audience Type")
    sel_a = [a for a in AUDIENCES if st.checkbox(a, key=f"a_{a}")]
    
    st.header("4. Age Range")
    sel_ag = [ag for ag in AGES if st.checkbox(ag, key=f"ag_{ag}")]
    
    # 4. SIDEBAR FOOTER (Save Feature Only)
    st.markdown("---")
    if "last_res" in st.session_state:
        st.download_button("💾 DOWNLOAD SET", st.session_state["last_res"], file_name="comedy_set.txt", use_container_width=True)
    else:
        st.button("💾 Save (Run First)", disabled=True, use_container_width=True)

# 4. MAIN UI
st.markdown("<h1 class='main-title'>🎤 COMEDY CROWD SIMULATOR</h1>", unsafe_allow_html=True)
bit = st.text_area("Your Material:", height=300, placeholder="Enter your jokes or bit here to see how your crowd will react...")

# 5. RUN LOGIC
if st.button("🚀 RUN SIMULATION", use_container_width=True):
    if city and sel_v:
        m_list = ["gemini-3-flash-preview", "gemini-1.5-flash"]
        success = False
        for m_name in m_list:
            try:
                temp = 0.1 if lock_mode else 0.7
                cfg = types.GenerateContentConfig(temperature=temp, top_p=0.95, max_output_tokens=2000)
                v_map = {1:"Hostile", 2:"Tough", 3:"Skeptical", 4:"Stiff", 5:"Normal", 6:"Warm", 7:"Friendly", 8:"Loving", 9:"On Fire", 10:"Legendary"}
                p = f"Act as audience. Venue: {sel_v}. City: {city}. Ages: {sel_ag}. Rules: {v_map[v_score]}. Bit: {bit}"
                with st.spinner(f"Testing {m_name}..."):
                    res = client.models.generate_content(model=m_name, contents=p, config=cfg)
                    st.session_state["last_res"] = res.text
                    success = True; break
            except Exception as e:
                if "503" in str(e) and m_name != m_list[-1]: continue
                st.error(f"Error: {e}"); break
        if success: st.rerun()
    else:
        st.warning("Select City and Venue!")

# 6. DISPLAY
if "last_res" in st.session_state:
    st.markdown("---")
    st.markdown(f"<div class='response-card'><h3>🎭 The Crowd Reacts:</h3>{st.session_state['last_res']}</div>", unsafe_allow_html=True)
