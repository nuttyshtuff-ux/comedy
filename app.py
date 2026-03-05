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
VENUES = ["Underground Comedy", "The Comedy Shop", "Don't Tell", "The College Gig", "Dive Bar", "Upscale Bar", "Comedy Showcase", "Open Mic Night", "Local Craft Brewery", "Wine Bar", "Opening for a Big Name"]
AUDIENCES = ["Normal", "Hostile/Heckling", "Distracted", "Drunk", "Passive", "New to Comedy", "Skeptical but Hopeful", "Jaded", "Friendly", "Silence for No Reason", "Easily Offended", "Chatty", "Other Comics Watching"]
AGES = ["Gen Z", "Millennials", "Gen X", "Boomers"]

# --- 3. THE SLIM TOP BAR (Now with Local References) ---
# Adjusted column ratios to fit 4 elements (3 toggles + 1 button)
c1, c2, c3, c4 = st.columns([2, 2, 2, 2])

with c1:
    lock_mode = st.checkbox("Lock Structure", value=True, help="✅ Checked: Precise feedback. ❌ Unchecked: Creative variations.")

with c2:
    coach_mode = st.checkbox("Coach Mode", value=False, help="Critique a joke or (if blank) get 5 premises.")

with c3:
    # THE NEW LOCAL REF TOGGLE
    local_ref_mode = st.checkbox("Local Refs", value=False, help=f"Inject specific landmarks, culture, and inside jokes for the selected city.")

with c4:
    if "last_response" in st.session_state:
        session_text = f"CITY: {st.session_state.get('last_city')}\n\nBIT:\n{st.session_state.get('last_bit')}\n\nFEEDBACK:\n{st.session_state['last_response']}"
        st.download_button("💾 Download", data=session_text, file_name="comedy_session.txt", use_container_width=True)
    else:
        st.button("💾 Save", disabled=True, use_container_width=True)

# --- 4. MAIN INTERFACE ---
st.title("🎤 Comedy Crowd Sim")
bit_text = st.text_area("Paste your set here:", height=250, placeholder="Drop your bit here... or leave blank for premises.")

# --- 5. SIDEBAR ---
with st.sidebar:
    st.title("🎤 Room Setup")
    city = st.text_input("City", value="San Luis Obispo")
    st.caption("Enter a City for the Local Vibe")
    
    st.markdown("---")
    st.header("1. The Venue")
    sel_venues = [v for v in VENUES if st.checkbox(v, key=f"v_{v}")]
    st.header("2. The Audience")
    sel_audiences = [a for a in AUDIENCES if st.checkbox(a, key=f"a_{a}")]
    st.header("3. Age Range")
    sel_ages = [ag for ag in AGES if st.checkbox(ag, key=f"ag_{ag}")]

# --- 6. EXECUTION ---
if st.button("🚀 Run Simulation / Generate Prompts", use_container_width=True):
    if sel_venues and sel_audiences and sel_ages:
        try:
            current_temp = 0.1 if lock_mode else 0.7
            config = types.GenerateContentConfig(
                temperature=current_temp,
                top_p=0.95,
                max_output_tokens=2048, 
            )

            # Logic for Local References
            local_instruction = ""
            if local_ref_mode:
                local_instruction = f"IMPORTANT: Suggest 3-5 specific local references, landmarks, or 'inside jokes' unique to {city} that would work for this specific venue/audience."

            if not bit_text.strip() and coach_mode:
                prompt = f"ACT AS A COMEDY WRITING PARTNER. {local_instruction} Suggest 5 premises for: VENUE: {sel_venues} | AUDIENCE: {sel_audiences} | AGES: {sel_ages} | CITY: {city}"
                spinner_msg = f"Fetching {city} premises..."
            else:
                coach_instr = "Include a 'COACH'S CORNER' feedback section." if coach_mode else ""
                prompt = f"ACT AS A COMEDY AUDIENCE SIMULATOR. {coach_instr} {local_instruction} VENUE: {sel_venues} | AUDIENCE: {sel_audiences} | AGES: {sel_ages} | CITY: {city} | BIT: {bit_text}"
                spinner_msg = "Simulating the room..."

            with st.spinner(spinner_msg):
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt,
                    config=config
                )
                st.session_state['last_response'] = response.text
                st.session_state['last_bit'] = bit_text if bit_text.strip() else "Writing Session"
                st.session_state['last_city'] = city
                
                st.markdown("---")
                st.markdown(response.text)
                if "100%" in response.text: st.balloons()
                st.rerun()
                
        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.warning("Please select Venue, Audience, and Age in the sidebar!")
