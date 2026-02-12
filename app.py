import streamlit as st
import google.generativeai as genai
import json
import os
from dotenv import load_dotenv

# --- INITIAL SETUP ---
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Load Dataset
with open('college_data.json', 'r') as f:
    college_data = json.load(f)
    college_context = json.dumps(college_data, indent=2)

# System Instruction for the AI
SYSTEM_PROMPT = f"""
You are the Admissions Assistant for Echelon Institute of Technology (EIT), Faridabad.
Answer questions based ONLY on this JSON data: {college_context}
Tone: Minimalist, professional, and helpful. 
If information is missing, refer them to {college_data['contact_info']['emails'][0]}.
"""

model = genai.GenerativeModel('gemini-1.5-flash', system_instruction=SYSTEM_PROMPT)

# --- STREAMLIT UI SETUP (Minimalist Design) ---
st.set_page_config(page_title="EIT Assistant", page_icon="🎓")

# Custom CSS for that flat, minimalist look you like
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    .stChatMessage { border-radius: 10px; border: 1px solid #333; margin-bottom: 10px; }
    .stTextInput input { background-color: #1e1e1e !important; color: white !important; border: 1px solid #444 !important; }
    h1 { font-family: 'Inter', sans-serif; font-weight: 700; letter-spacing: -1px; }
    </style>
    """, unsafe_allow_html=True)

st.title("EIT Admissions 🎓")
st.caption("Echelon Institute of Technology - Faridabad")

# Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- CHAT LOGIC ---
if prompt := st.chat_input("Ask about fees, courses, or scholarships..."):
    # User Message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Bot Message
    with st.chat_message("assistant"):
        response = model.generate_content(prompt)
        full_response = response.text
        st.markdown(full_response)
    
    st.session_state.messages.append({"role": "assistant", "content": full_response})
