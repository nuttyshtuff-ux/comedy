import streamlit as st
from google import genai
from google.genai import types

# 1. PAGE CONFIG
st.set_page_config(page_title="Comedy Crowd Simulator", page_icon="🎤", layout="wide")

# 2. CLIENT & DATA
api_key = st.secrets.get("api_key")
if not api_key:
    st.error("Missing API Key!")
    st.stop()
client = genai.Client(api_key=api_key)

VENUES = ["Underground Comedy", "The Comedy Shop", "Don't Tell", "The College Gig", "Dive Bar", "Upscale Bar", "Comedy Showcase", "Open Mic Night", "Local Craft Brewery", "Wine Bar", "Coffee Shop", "The Theater", "House Party", "Corporate Event", "Toastmasters", "Elk's Club", "Staff Meeting", "Opening for Big Name"]
AUDIENCES = ["Normal", "Hostile", "Distracted", "Drunk", "Passive", "New to Comedy", "Skeptical", "Jaded", "Friendly", "Easily Offended", "Chatty", "Other Comics"]
AGES = ["Gen Z", "Millennials", "Gen X", "Boomers"]

# 3. SIDEBAR (The Control Room)
with st.sidebar:
    st.title("🎤 Studio Controls")
    st.success("✅ Guest Access Active")
    
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
    
    # PayPal Link
    donate_url = "https://www.paypal.com/paypalme/mrcoward"
    st.markdown(f'[☕ Buy the Dev a Coffee]({donate_url})')

# 4. MAIN UI (High Legibility)
st.markdown("# 🎤 Comedy Crowd Simulator")
st.write("---")

bit = st.text_area(
    "Your Material:", 
    height=300, 
    placeholder="Enter your jokes or bit here to see how your crowd will react..."
)

# 5. RUN LOGIC
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
                
                with st.spinner(f"🎤 Testing the room via {m_name}..."):
                    res = client.models.generate_content(model=m_name, contents=p, config=cfg)
                    st.session_state["last_res"] = res.text
                    success = True
                    break
            except Exception as e:
                if "503" in str(e) and m_name != models[-1]:
                    st.warning("Crowd is rowdy (Server Busy)... pivoting.")
                    continue
                else:
                    st.error(f"Error: {e}")
                    break
        if success: st.rerun()
    else:
        st.warning("Please select City and Venue!")

# 6. DISPLAY (The "Stage")
if "last_res" in st.session_state:
    st.info("### 🎭 The Crowd Reacts:")
    st.markdown(st.session_state["last_res"])
