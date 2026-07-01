import streamlit as st
import random
import time
from chatbot import load_chain, get_response


st.title("Youtube Chatbot")

url = st.sidebar.text_input("Enter Youtube Video Link", type="default")

if url:
    if st.session_state.get("loaded_url") != url:
        chain = load_chain(url)
        if chain == None:
            print("No Transcript Found")
        else:
            st.session_state.loaded_url = url
            st.session_state.message = []
            st.session_state.chain = chain
            st.sidebar.success("Ready!")



def response_generator(ques, chain):
    response = get_response(ques, chain)
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
        res = st.write_stream(response_generator(prompt, st.session_state.chain))
        st.session_state.messages.append({"role" : "assistant" , "content" : res})


# Side bar
API_KEY = st.sidebar.text_input("API KEY", type="password")




