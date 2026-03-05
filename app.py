import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="AI/ML Tutor", layout="wide")
st.title("🎓 My Interactive ML Tutor")

with st.sidebar:
    api_key = st.text_input("Enter Google AI Key", type="password")
    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()

if api_key:
    try:
        genai.configure(api_key=api_key)
        # We use 'gemini-1.5-flash-latest' as it is the most stable 404-fix
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
        
        if "messages" not in st.session_state:
            st.session_state.messages = []

        for msg in st.session_state.messages:
            st.chat_message(msg["role"]).write(msg["content"])

        if prompt := st.chat_input("Ask your ML question here..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            st.chat_message("user").write(prompt)

            with st.chat_message("assistant"):
                try:
                    response = model.generate_content(f"Explain simply with code: {prompt}")
                    st.markdown(response.text)
                    st.session_state.messages.append({"role": "assistant", "content": response.text})
                except Exception as e:
                    st.error(f"AI Error: {e}. Try waiting 60 seconds.")
    except Exception as e:
        st.error(f"Configuration Error: {e}")
else:
    st.warning("Please enter your API key in the sidebar.")
