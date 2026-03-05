import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="AI/ML Tutor", layout="centered")
st.title("🎓 My Interactive ML Tutor")

# Sidebar for the Google API Key
with st.sidebar:
    st.header("Setup")
    api_key = st.text_input("Enter Google AI Key", type="password")
    st.info("Get a free key at aistudio.google.com")

if api_key:
    # Initialize the Gemini Brain
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.0-flash')

    # Session state keeps the chat history alive
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display the conversation
    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    # User input box
    if prompt := st.chat_input("Ask me anything about AI or Machine Learning!"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)

        # Send to AI and get a response
        with st.spinner("Tutor is thinking..."):
            response = model.generate_content(f"You are a patient ML tutor. Explain simply and provide a Python code snippet: {prompt}")
            answer = response.text
        
        st.session_state.messages.append({"role": "assistant", "content": answer})
        st.chat_message("assistant").write(answer)
else:
    st.warning("👈 Please enter your Google API key in the sidebar to start learning!")
