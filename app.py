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

# --- 4. MAIN ---
st.title("🎤 Comedy Crowd Sim")
bit_text = st.text_area("Paste your set here:", height=300, placeholder="Paste a joke to simulate... or leave blank with 'Coach Me' on for writing prompts.")

if st.button("🚀 Run Simulation / Generate Prompts", use_container_width=True):
    # Check if we have the minimum requirements (Audience selections)
    if sel_crowds and sel_ages and sel_vibes:
        try:
            temp_value = 0.1 if lock_mode else 0.8 # Slightly higher for prompts
            
            config = types.GenerateContentConfig(
                temperature=temp_value,
                top_p=0.95,
                max_output_tokens=1024,
            )

            # --- LOGIC: SIMULATE OR SUGGEST? ---
            if not bit_text.strip() and coach_mode:
                # WRITING PARTNER MODE
                prompt = f"""
                ACT AS A COMEDY WRITING PARTNER. 
                The user has no material yet. Based on the following room, suggest 5 specific comedy premises or 'seed' ideas.
                VENUE: {', '.join(sel_crowds)} | AGES: {', '.join(sel_ages)} | VIBE: {', '.join(sel_vibes)} | CITY: {city}
                
                Focus on:
                - Locally relevant topics for {city}.
                - Relatable hooks for {', '.join(sel_ages)}.
                - Edgy or observational angles that fit a {', '.join(sel_vibes)} vibe.
                
                STRUCTURE:
                1. WHY THIS ROOM IS TOUGH (Brief psych breakdown)
                2. 5 PREMISE SUGGESTIONS (Hook + Possible Angle)
                3. OPENING LINE IDEA
                """
                spinner_msg = "Brainstorming premises for this room..."
            
            elif bit_text.strip():
                # STANDARD SIMULATION MODE
                coach_instruction = f"Provide a 'COACH'S CORNER' for {', '.join(sel_ages)} in {', '.join(sel_crowds)}." if coach_mode else ""
                prompt = f"""
                ACT AS A COMEDY AUDIENCE SIMULATOR. 
                {coach_instruction} 
                VENUE: {', '.join(sel_crowds)} | AGES: {', '.join(sel_ages)} | VIBE: {', '.join(sel_vibes)} | CITY: {city}
                BIT: {bit_text}
                
                STRUCTURE:
                1. THE ROOM SOUND
                2. AUDIENCE PERSONAS
                3. IS IT FUNNY?
                4. SCORECARD (Laughter %, Tension %, Kill Probability %)
                5. THE TAG
                """
                spinner_msg = "Simulating the room..."
            else:
                st.warning("Please paste a joke or turn on 'Coach Me' for suggestions!")
                st.stop()

            with st.spinner(spinner_msg):
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt,
                    config=config
                )
                
                st.markdown("---")
                st.markdown(response.text)
                if "100%" in response.text: st.balloons()
                
        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.warning("Please check at least one box in every category (Audience, Age, and Vibe)!")
