import streamlit as st
import random
import time

st.title("Your Youtube Chatbot")


def response_generator():
    response = random.choice(
        [
            "Hello there! How can I assist you today?",
            "Hi, human! Is there anything I can help you with?",
            "Do you need help?",
        ]
    )
    for word in response.split():
        yield word + " "
        time.sleep(0.05)
    


if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("Say Something")

if prompt:
    with st.chat_message("User"):
        st.markdown(prompt)

    st.session_state.messages.append({"role" : "user", "content" : prompt})

    with st.chat_message("assistant"):
        res = st.write_stream(response_generator())
        st.session_state.messages.append({"role" : "assistant" , "content" : res})


# Side bar
API_KEY = st.sidebar.text_input("API KEY", type="password")
url = st.sidebar.text_input("Enter Youtube Video Link", type="default")



