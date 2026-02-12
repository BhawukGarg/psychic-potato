import streamlit as st
import google.generativeai as genai
import json

# --- 1. CONFIGURATION ---
# Using Streamlit's built-in secrets management for the API Key
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
except Exception as e:
    st.error("API Key not found. Please add GEMINI_API_KEY to Streamlit Secrets.")
    st.stop()

# Load the local JSON dataset
try:
    with open('college_data.json', 'r') as f:
        college_data = json.load(f)
        college_context = json.dumps(college_data, indent=2)
except FileNotFoundError:
    st.error("Error: 'college_data.json' not found in the repository.")
    st.stop()

# Define AI Persona
SYSTEM_PROMPT = f"""
You are the official Admissions Assistant for Echelon Institute of Technology (EIT), Faridabad.
Answer questions strictly based on this data: {college_context}
If you don't know the answer, refer them to {college_data['contact_info']['emails'][0]}.
Tone: Professional, helpful, and concise.
"""

model = genai.GenerativeModel('gemini-2.5-flash', system_instruction=SYSTEM_PROMPT)

# --- 2. MINIMALIST UI ---
st.set_page_config(page_title="EIT Bot", page_icon="🎓")

# Custom Minimalist Styling
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: white; }
    .stChatMessage { border: 1px solid #333; border-radius: 8px; }
    </style>
    """, unsafe_allow_html=True)

st.title("EIT Admissions Assistant 🎓")
st.caption("Ask about courses, fees, or scholarships.")

# Chat History initialization
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input
if prompt := st.chat_input("How can I help you today?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate Response
    with st.chat_message("assistant"):
        try:
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"AI Error: {e}")

