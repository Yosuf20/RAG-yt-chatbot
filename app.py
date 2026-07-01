import streamlit as st
import random
import time
from chatbot import get_response

import chatbot
print(dir(chatbot))

st.title("Youtube Chatbot")


def response_generator(ques):
    response = get_response(ques)
    for word in response.split():
        yield word + " "
        time.sleep(0.05)
    


if "messages" not in st.session_state:
    st.session_state.messages = []
    with st.chat_message("assistant"):
        st.markdown("Please Enter Vid Link")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("Say Something")

if prompt:
    
    with st.chat_message("User"):
        st.markdown(prompt)
        st.session_state.messages.append({"role" : "user", "content" : prompt})

    with st.chat_message("assistant"):
        res = st.write_stream(response_generator(prompt))
        st.session_state.messages.append({"role" : "assistant" , "content" : res})


# Side bar
API_KEY = st.sidebar.text_input("API KEY", type="password")
url = st.sidebar.text_input("Enter Youtube Video Link", type="default")



