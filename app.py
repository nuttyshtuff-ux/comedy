import streamlit as st
from google import genai
from google.genai import types

# 1. PAGE CONFIG & ENHANCED CSS
st.set_page_config(page_title="Comedy Crowd Simulator", page_icon="🎤", layout="wide")

st.markdown("""
<style>
    /* Main Background & Font */
    .stApp { background-color: #0e1117; color: #ffffff; }
    
    /* Title Styling */
    .main-title {
        font-size: 50px !important;
        font-weight: 800;
        color: #FF4B4B; /* "Mic Red" */
        text-align: center;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-bottom: 0px;
    }
    .sub-title {
        text-align: center;
        color: #808495;
        font-style: italic;
        margin-bottom: 30px;
    }

    /* Sidebar Polishing */
    [data-testid="stSidebar"] { background-color: #161b22; border-right: 1px solid #30363d; }
    .sidebar-footer { margin-top: auto; padding: 20px 0; border-top: 1px solid #30363d; }
    
    /* Input Box Focus */
    div[data-baseweb="textarea"] textarea { 
        background-color: #0d1117 !important; 
        color: #e6edf3 !important;
        border: 1px solid #30363d !important;
        border-radius: 10px !important;
    }

    /* Button "Glow" */
    .stButton button {
        background: linear-gradient(90deg, #FF4B4B 0%, #ff7b7b 100%) !important;
        color: white !important;
        border: none !important;
        transition: 0.3s all ease;
    }
    .stButton button:hover {
        transform: scale(1.02);
        box-shadow: 0px 4px 15px rgba(255, 75, 75, 0.4);
    }
</style>
""", unsafe_allow_html=True)

# 2. CLIENT & DATA (Unchanged logic)
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
    st.markdown("<h2 style='text-align: center; color: #FF4B4B;'>🎤 STUDIO</h2>", unsafe_allow_html=True)
    st.success("✅ GUEST ACCESS ACTIVE")
    
    with st.container():
        st.subheader("🛠️ Workshop Tools")
        lock_mode = st.checkbox("Lock Structure", value=True, help="Keep logic tight.")
        coach_mode = st.checkbox("Coach Mode", value=False, help="Technical feedback.")
        extend_mode = st.checkbox("Extend Bit", value=False, help="Generate next 3 mins.")
        local_ref_mode = st.checkbox("Local Refs", value=False, help="Use city landmarks.")
        
        st.markdown("---")
        st.subheader("📍 Room Setup")
        city = st.text_input("Current City", value="San Luis Obispo")
        st.caption("Sets the 'Local Vibe' logic.") 
        
        st.header("1. Venue")
        sel_v = [v for v in VENUES if st.checkbox(v, key=f"v_{v}")]
        
        st.header("2. Crowd Vibe")
        v_score = st.slider("Tough <-> Loving", 1, 10, 5)
        
        st.header("3. Audience Type")
        sel_a = [a for a in AUDIENCES if st.checkbox(a, key=f"a_{a}")]
        
        st.header("4. Age Range")
        sel_ag = [ag for ag in AGES if st.checkbox(ag, key=f"ag_{ag}")]

    # FOOTER WITH DONATE BUTTON
    st.markdown('<div class="sidebar-footer">', unsafe_allow_html=True)
    if "last_res" in st.session_state:
        st.download_button("💾 DOWNLOAD SET", data=st.session_state["last_res"], file_name="set.txt", use_container_width=True)
    
    # PAYPAL DONATE BUTTON
    donate_url = "https://www.paypal.com/paypalme/mrcoward"
    st.markdown(f'''
        <a href="{donate_url}" target="_blank" style="text-decoration: none;">
            <div style="background-color: #0070ba; color: white; text-align: center; padding: 12px; border-radius: 10px; font-weight: bold; margin-top: 10px;">
                ☕ Buy the Dev a Coffee
            </div>
        </a>''', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# 4. MAIN UI
st.markdown("<h1 class='main-title'>COMEDY CROWD SIMULATOR</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-title'>Test your bits against a digital room before you hit the stage.</p>", unsafe_allow_html=True)

bit = st.text_area("Your Material:", height=300, placeholder="Enter your jokes or bit here to see how your crowd will react...")

# 5. RUN LOGIC (With Fail-Safe)
if st.button("🚀 RUN SIMULATION", use_container_width=True):
    if city and sel_v:
        models = ["gemini-3-flash-preview", "gemini-1.5-flash"]
        success = False
        for m_name in models:
            try:
                temp = 0.1 if lock_mode else 0.7
                cfg = types.GenerateContentConfig(temperature=temp, top_p=0.95, max_output_tokens=2000)
                v_map = {1:"Hostile", 2:"Tough", 3:"Skeptical", 4:"Stiff", 5:"Normal", 6:"Warm", 7:"Friendly", 8:"Loving", 9:"On Fire", 10:"Legendary"}
                p = f"Act as comedy audience. Venue: {', '.join(sel_v)}. City: {city}. Ages: {', '.join(sel_ag)}. Audience: {', '.join(sel_a)}. Rules: Crowd is {v_map[v_score]}. Bit: {bit}"
                
                # CUSTOM SPINNER MESSAGE
                with st.spinner(f"✨ Testing the room with {m_name}..."):
                    res = client.models.generate_content(model=m_name, contents=p, config=cfg)
                    st.session_state["last_res"] = res.text
                    success = True
                    break
            except Exception as e:
                if "503" in str(e) and m_name != models[-1]:
                    st.warning("Crowd is rowdy (Server Busy)... pivoting to backup room.")
                    continue
                else:
                    st.error(f"Error: {e}")
                    break
        if success: st.rerun()
    else:
        st.warning("Please select City and Venue!")

# 6. DISPLAY
if "last_res" in st.session_state:
    st.markdown("---")
    st.markdown(f"<div style='background-color: #161b22; padding: 25px; border-radius: 15px; border: 1px solid #30363d;'>{st.session_state['last_res']}</div>", unsafe_allow_html=True)
