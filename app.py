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

# --- 3. SIDEBAR ---
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

    st.markdown("---")
    st.header("💡 Pro Mode")
    lock_mode = st.checkbox("Lock Structure (Deterministic)", value=True)
    st.caption("✅ **Checked:** Logical results. \n\n❌ **Unchecked:** Creative variations.")
    
    st.markdown(" ") 
    coach_mode = st.checkbox("Coach Me on This Room", value=False)
    st.caption("Grade a bit OR (if left blank) get premise suggestions.")

    # --- NEW: SAVE SESSION SECTION ---
    st.markdown("---")
    st.header("💾 Save Session")
    
    # We use session_state to keep track of the last response
    if "last_response" in st.session_state:
        # Create the text for the file
        session_text = f"""COMEDY CROWD SIM SESSION
---------------------------
CITY: {city}
VENUE: {', '.join(sel_crowds)}
AUDIENCE: {', '.join(sel_ages)}
VIBE: {', '.join(sel_vibes)}

ORIGINAL BIT:
{st.session_state.get('last_bit', 'N/A')}

---------------------------
SIMULATION FEEDBACK:
{st.session_state['last_response']}
---------------------------
"""
        st.download_button(
            label="Download Session (.txt)",
            data=session_text,
            file_name=f"comedy_sim_{city.replace(' ', '_')}.txt",
            mime="text/plain",
            use_container_width=True
        )
    else:
        st.caption("Run a simulation first to download the results.")

# --- 4. MAIN ---
st.title("🎤 Comedy Crowd Sim")
bit_text = st.text_area("Paste your set here:", height=300, placeholder="Paste a joke to simulate... or leave blank with 'Coach Me' on.")

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
                coach_instruction = f"Include a 'COACH'S CORNER' for {sel_ages} in {sel_crowds}." if coach_mode else ""
                prompt = f"ACT AS A COMEDY AUDIENCE SIMULATOR. {coach_instruction} VENUE: {sel_crowds} | AGES: {sel_ages} | VIBE: {sel_vibes} | CITY: {city} | BIT: {bit_text}"
                spinner_msg = "Simulating the room..."

            with st.spinner(spinner_msg):
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt,
                    config=config
                )
                
                # Store in session state for the download button
                st.session_state['last_response'] = response.text
                st.session_state['last_bit'] = bit_text if bit_text.strip() else "Brainstorming Session"
                
                st.markdown("---")
                st.markdown(response.text)
                if "100%" in response.text: st.balloons()
                
                # Rerun to update the sidebar with the download button
                st.rerun()
                
        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.warning("Please check at least one box in every category!")
