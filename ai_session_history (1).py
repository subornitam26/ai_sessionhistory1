import streamlit as st
import google.generativeai as genai

genai.configure(api_key = "GOOGLE_API_KEY")

model = genai.GenerativeModel("gemini-2.5-flash")

st.title("AI Chatbot with Session History")

if "messages" not in st.session_state:
    st.session_state.messages = []

if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("What can I do for you?"):
   
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        response = st.session_state.chat.send_message(prompt)
        reply = response.text
    except Exception as e:
        reply = f"Error calling Gemini: {str(e)}"

    st.session_state.messages.append({"role": "assistant", "content": reply})

    with st.chat_message("assistant"):
        st.markdown(reply)

if st.sidebar.button("Clear chat history"):
    st.session_state.messages = []
    st.session_state.chat = model.start_chat(history=[])
    st.rerun()