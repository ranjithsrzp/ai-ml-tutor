import streamlit as st
import google.generativeai as genai
import time

# 1. Page Configuration
st.set_page_config(page_title="AI/ML Interactive Tutor", layout="wide")
st.title("🎓 My Interactive ML Tutor")

# 2. Sidebar for API Key and Reset
with st.sidebar:
    st.header("Settings")
    api_key = st.text_input("Enter Google AI Key", type="password")
    st.info("Get a free key at aistudio.google.com")
    
    if st.button("Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

# 3. Initialize the Gemini Brain
if api_key:
    try:
        genai.configure(api_key=api_key)
        # Using 'gemini-1.5-flash' for higher free-tier limits
        model = genai.GenerativeModel('gemini-1.5-flash')
    except Exception as e:
        st.error(f"Configuration Error: {e}")

    # Initialize Session State for Chat
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display Conversation History
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # 4. Chat Input and AI Logic
    if prompt := st.chat_input("Ask me about AI/ML! (e.g., What is Gradient Descent?)"):
        # Add user message to history
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate Response with Error Handling
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            try:
                with st.spinner("Tutor is thinking..."):
                    # System instruction tells the AI HOW to behave
                    full_prompt = f"You are a patient, expert ML tutor. Explain this concept simply using analogies and always provide a short, clean Python code snippet: {prompt}"
                    response = model.generate_content(full_prompt)
                    
                    answer = response.text
                    message_placeholder.markdown(answer)
                    
                    # Add assistant message to history
                    st.session_state.messages.append({"role": "assistant", "content": answer})
            
            except Exception as e:
                # Specific check for Rate Limits (The error you saw)
                if "429" in str(e) or "ResourceExhausted" in str(e):
                    st.error("🚦 **Rate Limit Reached.** The free tier allows a few questions per minute. Please wait 60 seconds and try again.")
                elif "404" in str(e):
                    st.error("🔍 **Model Not Found.** Please check your model name or API key permissions.")
                else:
                    st.error(f"⚠️ An error occurred: {e}")
else:
    st.warning("👈 Please enter your Google API key in the sidebar to start your lesson!")
