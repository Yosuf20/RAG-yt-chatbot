import streamlit as st
import random
import time
from chatbot import load_chain, verify_key, validate_url, load_pdf, havepdf
import hashlib



st.title("Youtube Chatbot")

with st.sidebar:
    url = st.text_input("Enter Youtube Video Link", type="default")
    uploaded_file = st.file_uploader("Upload Your file") 



file_hash = hashlib.md5(uploaded_file.getvalue()).hexdigest()
 

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

elif uploaded_file:
        if st.session_state.get("file_hash") != file_hash:
            st.session_state["file_hash"] = file_hash 

    
            with st.spinner("Loading Transcript"):
                chain, retrieve = load_chain(uploaded_file)

            if chain is None:
                print("No Transcript Found")
            else:
                st.session_state.messages = []
                st.session_state.chain = chain
                st.session_state.retrieve = retrieve
                st.sidebar.success("Ready!")


# def response_generator(ques, chain, retrieve):
#     response = get_response(ques, chain, retrieve)
#     for word in response.split():
#         yield word + " "
#         time.sleep(0.05)
    

if "messages" not in st.session_state:
    st.session_state.messages = []
    with st.chat_message("assistant"):
        st.markdown("Please Enter Vid Link")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "responce_time" in message:
            st.caption(message['responce_time'])

prompt = st.chat_input("Say Something")

if prompt:
    start = time.time()
    with st.chat_message("user"):
        st.markdown(prompt)
        st.session_state.messages.append({"role" : "user", "content" : prompt})

    with st.chat_message("assistant"):
        
        res = st.write_stream(st.session_state.chain.stream(prompt))
        # res = st.write_stream(response_generator(prompt, st.session_state.chain, st.session_state.retrieve))
        res_time = time.time() - start
        st.info(f"Responce time {res_time} seconds")

        st.session_state.messages.append({"role" : "assistant" , "content" : res, 'responce_time' : res_time})