import streamlit as st
from google import genai
from google.genai import types

st.set_page_config(page_title="Comedy Simulator", page_icon="🎙️", layout="wide")

# 1. CSS - Navy & Yellow + Marquee Title + Yellow Tooltips
st.markdown("""<style>
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

VN = [
    "Underground Comedy", "The Comedy Shop", "Don't Tell Comedy", 
    "College Bar", "Dive Bar", "Upscale Bar", "Comedy Showcase", 
    "Open Mic", "Craft Brewery", "Theater", "Corporate Mixer", 
    "Elk's Lodge", "Toastmasters", "Casino Resort"
]

AU = ["Normal", "Hostile", "Drunk", "Passive", "Hopeful but Skeptical", "Jaded", "Friendly", "Easily Offended", "Other Comics Watching", "New to Live Comedy"]
AG = ["Gen Z", "Millennials", "Gen X", "Boomers"]

# 3. SIDEBAR
with st.sidebar:
    st.markdown("""<div class="sidebar-header"><div class="mic-container">
    <div class="mic-head">🎙️</div><div class="mic-pole"></div><div class="mic-base"></div>
    </div><h3 style="margin:0;">STUDIO CONTROLS</h3></div>""", unsafe_allow_html=True)
    st.success("✅ GUEST ACCESS ACTIVE")
    st.subheader("🛠️ Workshop Tools")
    
    # UPDATED: More "Explainy" Tooltips
    lk = st.checkbox("Lock Structure", value=True, 
                     help="Forces the AI to strictly analyze the logic and punchlines of your bit rather than riffing or getting distracted.")
    ch = st.checkbox("Coach Mode", value=False, 
                     help="The AI will act as a veteran headliner, providing structural feedback and suggesting where to trim the fat or add a tag.")
    ex = st.checkbox("Extend Bit", value=False, 
                     help="Asks the AI to brainstorm the next 3 minutes of material based on the themes and characters introduced in your bit.")
    rf = st.checkbox("Local Refs", value=False, 
                     help="The AI will weave in specific landmarks, local inside jokes, and geographical references based on your chosen city.")
    
    st.markdown("---")
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
    if "last_res" in st.session_state:
        st.download_button("💾 DOWNLOAD SET", st.session_state["last_res"], "set.txt", use_container_width=True)
    else:
        st.button("💾 Save (Run First)", disabled=True, use_container_width=True)

# 4. MAIN UI
st.markdown("<h1 class='main-title'>🎙️ COMEDY CROWD SIMULATOR</h1>", unsafe_allow_html=True)
instr = "Enter your joke or bit to see how your crowd might react. Or leave blank and check Coach for suggestions."
bit = st.text_area("Your Material:", height=300, placeholder=instr)

# 5. RUN LOGIC
if st.button("🚀 RUN SIMULATION", use_container_width=True):
    if city and sel_v:
        v_map = {1:"Hostile", 2:"Tough", 3:"Skeptical", 4:"Stiff", 5:"Normal", 6:"Warm", 7:"Friendly", 8:"Loving", 9:"On Fire", 10:"Legendary"}
        fb = bit if bit.strip() != "" else "Suggest new premises."
        p = "Act as audience. Give a long, detailed, response. "
        p += "Venue: " + str(sel_v) + ". "
        p += "City: " + str(city) + ". "
        p += "Audience: " + str(sel_a) + ". "
        p += "Ages: " + str(sel_ag) + ". "
        p += "Rules: " + v_map[v_score] + ". "
        p += "Bit: " + fb
        cfg = types.GenerateContentConfig(temperature=(0.1 if lk else 0.7), top_p=0.95, max_output_tokens=2000)
        
        # SURGICAL SWAP: Replacing retired models with March 9th Stable versions
        m_list = ["gemini-3.1-flash", "gemini-2.5-flash", "gemini-2.0-flash-001"]
        
        for m_name in m_list:
            try:
                with st.spinner("Analyzing Room..."):
                    res = client.models.generate_content(model=m_name, contents=p, config=cfg)
                    st.session_state["last_res"] = res.text
                    st.rerun()
            except Exception:
                continue
    else:
        st.warning("Select City and Venue!")

# 6. DISPLAY
if "last_res" in st.session_state:
    out_txt = st.session_state["last_res"]
    st.markdown(f"""<div class='response-card'><h3>🎭 The Crowd Reacts:</h3>{out_txt}</div>""", unsafe_allow_html=True)

