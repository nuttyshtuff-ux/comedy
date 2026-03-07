import streamlit as st
from google import genai
from google.genai import types

st.set_page_config(page_title="Comedy Crowd Simulator", page_icon="🎙️", layout="wide")

# 1. CSS - Navy & Yellow with Custom Mic Stand
st.markdown("""<style>
    .main-title { color: #1e3a8a; font-weight: 800; text-align: center; }
    .mic-container {
        display: flex; flex-direction: column; align-items: center;
        justify-content: center; line-height: 0.8; margin-right: 10px;
    }
    .mic-head { font-size: 24px; margin-bottom: -2px; }
    .mic-pole { background-color: #facc15; width: 3px; height: 12px; margin-bottom: -1px; }
    .mic-base { background-color: #facc15; width: 14px; height: 3px; border-radius: 2px; }
    .sidebar-header { display: flex; align-items: center; justify-content: center; margin-bottom: 20px; }
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
    st.markdown("""
        <div class="sidebar-header">
            <div class="mic-container">
                <div class="mic-head">🎙️</div>
                <div class="mic-pole"></div>
                <div class="mic-base"></div>
            </div>
            <h3 style="margin:0; letter-spacing: 1px;">STUDIO CONTROLS</h3>
        </div>
    """, unsafe_allow_html=True)
    st.success("✅ GUEST ACCESS ACTIVE")
    st.subheader("🛠️ Workshop Tools")
    lock_mode = st.checkbox("Lock Structure", value=True)
    coach_mode = st.checkbox("Coach Mode", value=False)
    extend_mode = st.checkbox("Extend Bit", value=False)
    local_ref_mode = st.checkbox("Local Refs", value=False)
    st.markdown("---")
    city = st.text_input("City", value="San Luis Obispo")
    sel_v = [v for v in VENUES if st.checkbox(v, key=f"v_{v}")]
    v_score = st.slider("Tough <-> Loving", 1, 10, 5)
    sel_a = [a for a in AUDIENCES if st.checkbox(a, key=f"a_{a}")]
    sel_ag = [ag for ag in AGES if st.checkbox(ag, key=f"ag_{ag}")]
    st.markdown("---")
    if "last_res" in st.session_state:
        st.download_button("💾 DOWNLOAD SET", st.session_state["last_res"], file_name="comedy_set.txt", use_container_width=True)
    else:
        st.button("💾 Save (Run First)", disabled=True, use_container_width=True)

# 4. MAIN UI
st.markdown("<h1 class='main-title'>🎙️ COMEDY CROWD SIMULATOR</h1>", unsafe_allow_html=True)

# UPDATED: More explicit instructions including the Coach fallback
bit = st.text_area(
    "Your Material:", 
    height=300, 
    placeholder="Enter your joke or bit here to see how it might land with your crowd... Or check Coach and leave blank for suggestions."
)

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
                
                # Logic to handle blank input if Coach Mode is on
                final_bit = bit if bit.strip() != "" else "I am out of ideas. Give me a premise or a few jokes to try based on this specific crowd and venue."
                
                p = f"Act as audience. Venue: {sel_v}. City: {city}. Ages: {sel_ag}. Rules: {v_map[v_score]}. Bit: {final_bit}"
                with st.spinner(f"🎤 Crowdsourcing feedback via {m_name}..."):
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
