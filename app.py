import streamlit as st
from google import genai
from google.genai import types

# --- 1. SETUP ---
st.set_page_config(page_title="Comedy Crowd Simulator", page_icon="🎤", layout="wide")

# --- CUSTOM CSS: Centering & SMART Mobile Label ---
st.markdown("""
    <style>
    /* 1. Center the Main Title */
    .stApp h1 {
        text-align: center;
        width: 100%;
    }

    /* 2. SMART "Options" label: ONLY shows on Mobile (< 992px) */
    @media (max-width: 991px) {
        [data-testid="stHeader"]::before {
            content: 'Options';
            position: absolute;
            left: 50px;
            top: 15px;
            font-weight: bold;
            font-size: 16px;
            color: #31333F; 
        }
    }

    /* 3. Mobile font fix & Button styling */
    div[data-baseweb="textarea"] textarea { font-size: 16px !important; }
    .stButton button {
        height: 3.5em;
        border-radius: 10px;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# ... [The rest of the code remains exactly the same] ...
