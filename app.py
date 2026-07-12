import streamlit as st
import random
import time
from chatbot import load_chain, get_response, verify_key, validate_url


st.title("Youtube Chatbot")

url = st.sidebar.text_input("Enter Youtube Video Link", type="default")


if url:
    if st.session_state.get("loaded_url") != url:

        with st.sidebar.spinner("Verifying Youtube Link Url..."):
            valid = validate_url(url)

        if not valid:
            st.sidebar.error("Invalid Youtube Link. Pls Enter a Valid URL")

        else:
            with st.spinner("Loading Transcript"):
                chain, retrieve = load_chain(url)

            if chain is None:
                print("No Transcript Found")
            else:
                st.session_state.loaded_url = url
                st.session_state.messages = []
                st.session_state.chain = chain
                st.session_state.retrieve = retrieve
                st.sidebar.success("Ready!")


def response_generator(ques, chain, retrieve):
    response = get_response(ques, chain, retrieve)
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

    with st.chat_message("user"):
        st.markdown(prompt)
        st.session_state.messages.append({"role" : "user", "content" : prompt})

    with st.chat_message("assistant"):
        res = st.write_stream(response_generator(prompt, st.session_state.chain, st.session_state.retrieve))
        st.session_state.messages.append({"role" : "assistant" , "content" : res})