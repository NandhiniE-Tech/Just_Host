import streamlit as st #this is working code use this file alone mstr, not any other
from RetrieverPrompt import get_answer

st.title('Bharathi\'s Chatbot தமிழர் பாரம்பரியம்')

# Function for generating LLM response
import requests
import streamlit as st

FASTAPI_URL = "http://127.0.0.1:8000/chat"


def generate_response(input_text):
    try:
        response = requests.post(FASTAPI_URL, json={"user_input": input_text})
        if response.status_code == 200:
            return response.json()["response"]
        else:
            st.error(f"❌ FastAPI Error: {response.text}")
            return "Error in processing request."
    except Exception as e:
        st.error(f"❌ Connection Error: {e}")
        return "Server unreachable."

# Initialize conversation history in session state
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "வணக்கம்! நான் பாரதி. உங்களுக்கு எப்படி உதவ முடியும்?"}]

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# User-provided prompt
if prompt := st.chat_input():
    # Add user message to chat
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    # Generate and display assistant response
    with st.chat_message("assistant"):
        with st.spinner("பதில் தயாராகிறது..."):
            response = generate_response(prompt)
            st.write(response)
            st.session_state.messages.append({"role": "assistant", "content": response})