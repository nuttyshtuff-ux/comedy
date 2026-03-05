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

# --- 3. THE SLIM TOP BAR ---
c1, c2, c3, c4, c5 = st.columns([1.5, 1.5, 1.5, 1.5, 2])

with c1:
    lock_mode = st.checkbox("Lock Structure", value=True, help="✅ Checked: Precise feedback. ❌ Unchecked: Creative variations.")

with c2:
    coach_mode = st.checkbox("Coach Mode", value=False, help="Critique a joke or (if blank) get 5 premises.")

with c3:
    extend_mode = st.checkbox("Extend Bit", value=False, help="Suggest 3-5 ways to keep the joke going.")

with c4:
    local_ref_mode = st.checkbox("Local Refs", value=False, help="Inject landmarks and inside jokes for the city.")

with c5:
    if "last_response" in st.session_state:
        session_text = f"CITY: {st.session_state.get('last_city')}\n\nBIT:\n{st.session_state.get('last_bit')}\n\nFEEDBACK:\n{st.session_state['last_response']}"
        st.download_button("💾 Download", data=session_text, file_name="comedy_session.txt", use_container_width=True)
    else:
        st.button("💾 Save", disabled=True, use_container_width=True)

# --- 4. MAIN INTERFACE ---
st.title("🎤 Comedy Crowd Sim")
bit_text = st.text_area("Paste your set here:", height=250, placeholder="Drop your bit here...")

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

            # Build instructions
            instructions = []
            if coach_mode: instructions.append("Include a 'COACH'S CORNER' feedback section.")
            if extend_mode: instructions.append("Add a section 'THE NEXT 3 MINUTES' to expand this bit.")
            if local_ref_mode: instructions.append(f"Suggest specific local references for {city}.")
            
            instr_str = " ".join(instructions)
            venue_str = ", ".join(sel_venues)
            aud_str = ", ".join(sel_audiences)
            age_str = ", ".join(sel_ages)

            # --- THE LOGIC BLOCK ---
            if not bit_text.strip() and coach_mode:
                prompt = f"ACT AS A COMEDY WRITING PARTNER. {instr_str} Suggest 5 premises for: VENUE: {venue_str} | AUDIENCE: {aud_str} | AGES: {age_str} | CITY: {city}"
                spinner_msg = f"Brainstorming {city} ideas..."
            else:
                # THIS IS THE BLOCK THAT WAS BROKEN
                prompt = f"ACT AS A COMEDY AUDIENCE SIMULATOR. {instr_str} VENUE: {venue_str} | AUDIENCE: {aud_str} | AGES: {age_str} | CITY: {city} | BIT: {bit_text}"
                spinner_msg = "Simulating and Expanding..."

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
