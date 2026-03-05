import streamlit as st
from google import genai
from google.genai import types

# --- 1. SETUP ---
st.set_page_config(page_title="Comedy Crowd Sim", page_icon="🎤", layout="wide")

api_key = st.secrets.get("api_key")
if not api_key:
    st.error("Missing API Key in Streamlit Secrets!")
    st.stop()

client = genai.Client(
    api_key=api_key,
    http_options={'api_version': 'v1'}
)

# --- 2. DATA ---
CROWDS = ["Underground Comedy", "The Comedy Shop", "Don't Tell", "The College Gig", "Dive Bar", "Upscale Bar", "Comedy Showcase", "Open Mic Night"]
AGES = ["Gen Z", "Millennials", "Gen X", "Boomers"]
VIBES = ["Normal", "Hostile/Heckling", "Distracted", "Drunk", "Passive", "New to Comedy", "Skeptical but Hopeful", "Jaded", "Friendly", "Silence for No Reason", "Easily Offended", "Chatty", "Other Comics Watching"]

# --- 3. THE SLIM TOP BAR ---
_, c1, c2, c3, _ = st.columns([1, 2, 2, 2, 1])

with c1:
    lock_mode = st.checkbox(
        "Lock Structure", 
        value=True, 
        help="✅ Checked: Precise, reliable feedback format. ❌ Unchecked: Creative, unpredictable 'wildcard' responses."
    )

with c2:
    coach_mode = st.checkbox(
        "Coach Mode", 
        value=False, 
        help="Paste a joke for a critique, or leave the area blank to get 5 premise suggestions for this specific room."
    )

with c3:
    # UPDATED TOOLTIP FOR SAVE/DOWNLOAD
    save_help = "Download a .txt file containing your joke, the room settings, and the simulation results."
    if "last_response" in st.session_state:
        session_text = f"CITY: {st.session_state.get('last_city')}\n\nBIT:\n{st.session_state.get('last_bit')}\n\nFEEDBACK:\n{st.session_state['last_response']}"
        st.download_button(
            "💾 Download", 
            data=session_text, 
            file_name="comedy_session.txt", 
            use_container_width=True,
            help=save_help
        )
    else:
        st.button("💾 Save", disabled=True, use_container_width=True, help=save_help)

# --- 4. MAIN TITLE & INPUT ---
st.title("🎤 Comedy Crowd Sim")

bit_text = st.text_area("Paste your set here:", height=250, placeholder="Drop your bit here... or leave blank with 'Coach Mode' on for premises.")

# --- 5. SIDEBAR ---
with st.sidebar:
    st.title("🎤 Room Setup")
    city = st.text_input("City", value="San Luis Obispo")
    st.caption("Enter a City for the Local Vibe")
    
    st.markdown("---")
    st.header("1. The Audience")
    sel_crowds = [c for c in CROWDS if st.checkbox(c, key=f"c_{c}")]
    
    st.header("2. Age Range")
    sel_ages = [a for a in AGES if st.checkbox(a, key=f"a_{a}")]
    
    st.header("3. The Vibe")
    sel_vibes = [v for v in VIBES if st.checkbox(v, key=f"v_{v}")]

# --- 6. EXECUTION ---
if st.button("🚀 Run Simulation / Generate Prompts", use_container_width=True):
    if sel_crowds and sel_ages and sel_vibes:
        try:
            current_temp = 0.1 if lock_mode else 0.7
            config = types.GenerateContentConfig(
                temperature=current_temp,
                top_p=0.95,
                max_output_tokens=2048, 
            )

            if not bit_text.strip() and coach_mode:
                prompt = f"ACT AS A COMEDY WRITING PARTNER. Suggest 5 premises for: VENUE: {sel_crowds} | AGES: {sel_ages} | VIBE: {sel_vibes} | CITY: {city}"
                spinner_msg = f"Fetching {city} premises..."
            else:
                coach_instruction = "Include a 'COACH'S CORNER' feedback section." if coach_mode else ""
                prompt = f"ACT AS A COMEDY AUDIENCE SIMULATOR. {coach_instruction} VENUE: {sel_crowds} | AGES: {sel_ages} | VIBE: {sel_vibes} | CITY: {city} | BIT: {bit_text}"
                spinner_msg = "Simulating the room..."

            with st.spinner(spinner_msg):
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt,
                    config=config
                )
                st.session_state['last_response'] = response.text
                st.session_state['last_bit'] = bit_text if bit_text.strip() else "Brainstorming Session"
                st.session_state['last_city'] = city
                
                st.markdown("---")
                st.markdown(response.text)
                if "100%" in response.text: st.balloons()
                st.rerun()
                
        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.warning("Please select Audience, Age, and Vibe in the sidebar!")
