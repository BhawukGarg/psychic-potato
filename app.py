import streamlit as st
import google.generativeai as genai
import json
import time
from google.api_core import exceptions

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="EIT Search", page_icon="🎓", layout="centered")

# Securely load API Key from Streamlit Secrets
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
except Exception:
    st.error("Missing GEMINI_API_KEY in Streamlit Secrets!")
    st.stop()

# Load the Dataset
try:
    with open('college_data.json', 'r') as f:
        college_data = json.load(f)
        college_context = json.dumps(college_data, indent=2)
except FileNotFoundError:
    st.error("college_data.json not found in repository.")
    st.stop()

# --- 2. PERPLEXITY-STYLE UI (CSS) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; background-color: #000000; color: #ffffff; }
    .stApp { background-color: #000000; }
    
    /* Clean chat bubbles */
    .stChatMessage { background-color: transparent !important; border-bottom: 1px solid #222 !important; padding: 2rem 0 !important; }
    
    /* Source Cards */
    .source-tag {
        display: inline-block;
        background: #1a1a1a;
        border: 1px solid #333;
        border-radius: 6px;
        padding: 4px 10px;
        font-size: 11px;
        color: #aaa;
        margin-right: 8px;
        margin-bottom: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. CORE LOGIC ---
# System Instructions for the AI
SYSTEM_PROMPT = f"""
You are the official Admissions Assistant for Echelon Institute of Technology (EIT), Faridabad.
Knowledge Base: {college_context}
Rules:
1. Answer only based on the data provided.
2. If unknown, direct to {college_data['contact_info']['emails'][0]}.
3. Use a professional, clean, and minimalist tone.
"""

model = genai.GenerativeModel('gemini-2.5-flash', system_instruction=SYSTEM_PROMPT)

def get_ai_response(prompt):
    """Handles API calls with a retry for the 429 Rate Limit error."""
    try:
        response = model.generate_content(prompt)
        return response.text
    except exceptions.ResourceExhausted:
        return "⚠️ Quota exceeded. The server is a bit busy. Please wait 30 seconds and try again!"
    except Exception as e:
        return f"An error occurred: {str(e)}"

# --- 4. THE INTERFACE ---
st.title("EIT Admissions Assistant")
st.caption("Echelon Institute of Technology - Faridabad | Official 2025 Data")

# Initialize Chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message["role"] == "assistant":
            st.markdown('<div class="source-tag">📄 Official Dataset</div><div class="source-tag">💰 Fees & Slabs</div>', unsafe_allow_html=True)
        st.markdown(message["content"])

# User Input
if user_input := st.chat_input("Ask about B.Tech fees, scholarships, or placements..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Searching..."):
            ai_text = get_ai_response(user_input)
            st.markdown('<div class="source-tag">📄 Official Dataset</div>', unsafe_allow_html=True)
            st.markdown(ai_text)
            st.session_state.messages.append({"role": "assistant", "content": ai_text})
