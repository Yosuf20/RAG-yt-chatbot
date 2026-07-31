# !pip install langchain faiss-cpu tiktoken langchain_huggingface langchain_community langchain-core -q youtube-transcript-api python-dotenv langchain_groq
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableParallel, RunnableLambda, RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
from langchain_community.vectorstores import FAISS
from curl_cffi import requests as curl_requests
import os
from langchain_ollama import ChatOllama
from dotenv import load_dotenv
load_dotenv()
import time
from deep_translator import GoogleTranslator
import tempfile


def get_yt_client():
    session = curl_requests.Session(impersonate="chrome110")
    return YouTubeTranscriptApi(http_client=session)



def vid_id(url : str) -> str:
    video_id = url.split("=")[1].split("&")[0]
    return video_id


def get_llm(api : str | None = None):
        llm = ChatOllama(
        model="qwen3:4b",
        temperature = 1.5,
        think = False,
        num_ctx=2048,
        repeat_penalty=1.1
        )
        return llm

# Loading Pdf 

def havepdf():
    return 


def load_pdf(uploaded_file):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(uploaded_file.getvalue())
        temp_path = tmp.name

    loader = PyMuPDFLoader(file_path=temp_path, extract_images=True, )
    documents = loader.load()

    # print(len(documents))
    # print(documents[0].page_content)
    # print(documents[0].metadata)
    # print("---------------------------------")
    # print(documents[1].page_content)
    # print(documents[2].metadata)

    text = "\n".join(chunk.page_content for chunk in documents)

    return text




def verify_key(key : str) -> bool:
    try:
        llm = ChatOllama(
            model="qwen4:4b",
            max_tokens=1
        )
        llm.invoke("Hello")
        return True
    except Exception as e:
        print(f"Error : {e}")
        return False
    
def validate_url(url : str) -> bool:
    try:
        yt = get_yt_client()
        trans_list = yt.fetch(
            video_id=vid_id(url),
            languages=['en', 'hi']
        )
        return True
    except Exception as e:
        print(f"Error : {e}")
        return False
    

def get_transcript(url : str) -> str | None:
    t1 = time.time()
    ytt_api = get_yt_client()
    
    transcript_list = ytt_api.list(
            video_id = vid_id(url),
            )
    
    try:
        transcript = transcript_list.find_transcript(['en']).fetch()

        return ''.join(chunk.text for chunk in transcript)

    except Exception as e:

        transcript = ytt_api.fetch(video_id=vid_id(url), languages=['hi'])

        translated = []

        translator = GoogleTranslator(
            source="auto",
            target="en"
        )

        for chunk in transcript:
            translated.append(
                translator.translate(chunk.text)
            )

        english = ' '.join(translated)


        print(f"Time Taken in Translation {time.time() - t1}")
        return english
        print(f"Error {e}")


def load_chain(script, url: str | None = None, API_KEY : str | None = None):

    if url:
        transcript = get_transcript(url)
        if transcript is None:
            return None
    else:
        transcript = load_pdf(script)
        
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    print(type(transcript))
    chunks = splitter.create_documents([transcript])

    embeddings = HuggingFaceEmbeddings( 
        model="BAAI/bge-small-en-v1.5",
        # model_kwargs ={'device':'cuda'}
    )

    vector_store = FAISS.from_documents(
        embedding= embeddings,
        documents=chunks,
    )

    retriever = vector_store.as_retriever(
        search_type='mmr',
        search_kwargs={'k':4}
    )

    prompt = PromptTemplate(
        template="""
        You are a helpful Youtube video chatbot
        Answer only from the provided transcript context
        If the context is insufficeint then simply say i dont know

        {context}
        Question: {question}
        """,
        input_variables=['context', 'question']
    )

    llm = get_llm(API_KEY)

    def format_docs(content):
        context_text = "\n\n".join(doc.page_content for doc in content)
        return context_text

    parallel_chain = RunnableParallel({
        'context' : retriever | RunnableLambda(format_docs),
        'question' : RunnablePassthrough()
    })

    
    parser = StrOutputParser()
   
    chain = parallel_chain | prompt | llm 

    retrieve = parallel_chain
    return chain, retrieve


# def get_response(question : str, chain, retrive) -> str:
#    start = time.time()

#    docs = retrive.invoke(question)
#    print(docs)
#    print(len(docs['context']))
#    print("Retrieval:", time.time() - start)


#    start = time.time()
#    response = chain.invoke(question)
#    print("Generation:", time.time() - start)
#    return response.content


