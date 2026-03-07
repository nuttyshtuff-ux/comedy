import streamlit as st
from google import genai
from google.genai import types

st.set_page_config(page_title="Comedy Simulator", page_icon="🎙️", layout="wide")

# 1. CSS - Navy & Yellow + Marquee + Tooltip Filter
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

VN = ["Underground", "Comedy Shop", "Don't Tell", "College", "Dive Bar", "Upscale", "Showcase", "Open Mic", "Brewery", "Theater", "House", "Corp"]
AU = ["Normal", "Hostile", "Drunk", "Passive", "Skeptical", "Jaded", "Friendly", "Offended", "Comics"]
AG = ["Gen Z", "Millennials", "Gen X", "Boomers"]

# 3. SIDEBAR
with st.sidebar:
    st.markdown("""<div class="sidebar-header"><div class="mic-container">
    <div class="mic-head">🎙️</div><div class="mic-pole"></div><div class="mic-base"></div>
    </div><h3 style="margin:0;">STUDIO</h3></div>""", unsafe_allow_html=True)
    
    st.subheader("Tools")
    lk = st.checkbox("Lock", value=True, help="Keeps AI on joke logic.")
    ch = st.checkbox("Coach", value=False, help="Adds feedback.")
    ex = st.checkbox("Extend", value=False, help="Next 3 mins.")
    rf = st.checkbox("Local", value=False, help="City landmarks.")
    
    st.markdown("---")
    city = st.text_input("City", value="San Luis Obispo")
    st.caption("Enter City for Local Vibe")
    
    st.header("Venue")
    s_v = [v for v in VN if st.checkbox(v, key=f"v_{v}")]
            
    st.header("Vibe")
    v_s = st.slider("Tough-Loving", 1, 10, 5)
    
    st.header("Crowd")
    s_a = [a for a in AU if st.checkbox(a, key=f"a_{a}")]
            
    st.header("Age")
    s_g = [g for g in AG if st.checkbox(g, key=f"g_{g}")]
    
    st.markdown("---")
    if "last_res" in st.session_state:
        st.download_button("💾 SAVE SET", st.session_state["last_res"], "set.txt")
    else:
        st.button("💾 Save (Run First)", disabled=True)

# 4. MAIN UI
t_h = "<h1 class='main-title'>🎙️ COMEDY SIMULATOR</h1>"
st.markdown(t_h, unsafe_allow_html=True)

bit = st.text_area("", height=350, placeholder="Enter joke... Or check Coach and leave blank.")

# 5. RUN LOGIC
if st.button("🚀 RUN SIMULATION", use_container_width=True):
    if city and s_v:
        fb = bit if bit.strip() != "" else "Suggest new premises."
        cfg = types.GenerateContentConfig(temperature=(0.1 if lk else 0.7), top_p=0.95, max_output_tokens=2000)
        v_m = {1:"Hostile", 2:"Tough", 3:"Skeptical", 4:"Stiff", 5:"Normal", 6:"Warm", 7:"Friendly", 8:"Loving", 9:"On Fire", 10:"Legendary"}
        p = f"Act as audience. Venue: {s_v}. City: {city}. Ages: {s_g}. Rules: {v_m[v_s]}. Bit: {fb}"
        
        m_list = ["gemini-3-flash-preview", "gemini-1.5-flash"]
        for m_n in m_list:
            try:
                with st.spinner(f"Testing {m_n}..."):
                    res = client.models.generate_content
