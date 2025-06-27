import streamlit as st
import requests

st.set_page_config(page_title="AI Booking Agent")
st.title("🗓️ Book an Appointment")

if "chat" not in st.session_state:
    st.session_state.chat = []

user_input = st.text_input("You:", "")

if st.button("Send") and user_input:
    st.session_state.chat.append(("You", user_input))
    try:
        res = requests.post("http://localhost:8000/chat/", json={"message": user_input})
        if res.status_code == 200:
            reply = res.json().get("response", "No reply from agent.")
            st.session_state.chat.append(("Agent", reply))
        else:
            st.session_state.chat.append(("Agent", f"Error: {res.status_code} - {res.text}"))
    except Exception as e:
        st.session_state.chat.append(("Agent", f"Exception: {str(e)}"))

for sender, msg in st.session_state.chat:
    st.markdown(f"**{sender}**: {msg}")

