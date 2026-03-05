import streamlit as st
import google.generativeai as genai

# Page Setup
st.set_page_config(page_title="AI/ML Tutor", layout="wide")
st.title("🎓 My Interactive ML Tutor")

with st.sidebar:
    st.header("Setup")
    api_key = st.text_input("Enter Google AI Key", type="password")
    if st.button("Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

if api_key:
    try:
        genai.configure(api_key=api_key)
        
        # FIX: We use 'gemini-pro' or 'gemini-1.5-flash' WITHOUT extra tags
        # These are the most universally accepted names in the Google API
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        if "messages" not in st.session_state:
            st.session_state.messages = []

        for msg in st.session_state.messages:
            st.chat_message(msg["role"]).write(msg["content"])

        if prompt := st.chat_input("Ask me about AI/ML!"):
            st.session_state.messages.append({"role": "user", "content": prompt})
            st.chat_message("user").write(prompt)

            with st.chat_message("assistant"):
                try:
                    # Added a safety check for the response
                    response = model.generate_content(f"Explain simply with code: {prompt}")
                    if response.text:
                        st.markdown(response.text)
                        st.session_state.messages.append({"role": "assistant", "content": response.text})
                except Exception as e:
                    if "ResourceExhausted" in str(e):
                        st.error("🚦 Busy! Please wait 60 seconds.")
                    else:
                        st.error(f"AI Error: {e}")
    except Exception as e:
        st.error(f"Configuration Error: {e}")
else:
    st.warning("👈 Enter your key in the sidebar!")
