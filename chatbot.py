
# !pip install langchain faiss-cpu tiktoken langchain_huggingface langchain_community langchain-core -q youtube-transcript-api python-dotenv langchain_groq

from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableParallel, RunnableLambda, RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
from langchain_community.vectorstores import FAISS
import os
from dotenv import load_dotenv
load_dotenv()




def vid_id(url : str) -> str:
    video_id = url.split("=")[1].split("&")[0]
    return video_id

def get_llm(api : str):
    if api:
        llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        api_key=api
        )
        return llm
    else:
        llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        api_key=os.getenv("GROQ_API_KEY")
        )
    
def verify_key(key : str) -> bool:
    try:
        llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            api_key=key,
            max_tokens=1
        )
        llm.invoke("Hello")
        return True
    except Exception as e:
        return False
    

def get_transcript(url : str) -> str | None:
    try:
        ytt_api = YouTubeTranscriptApi()

        transcript_list = ytt_api.fetch(
            video_id = vid_id(url),
            languages=['en']
            )
        transcript = " ".join(chunk.text for chunk in transcript_list)
        return transcript
    except:
        print("No caption available")


def load_chain(url: str, API_KEY : str | None):
    
    transcript = get_transcript(url)
    if transcript is None:
        return None
    
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = splitter.create_documents([transcript])

    embeddings = HuggingFaceEmbeddings( model="BAAI/bge-small-en-v1.5")

    vector_store = FAISS.from_documents(
        embedding= embeddings,
        documents=chunks

    )

    retriever = vector_store.as_retriever(
        search_type='similarity',
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

    return chain


def get_response(question : str, chain) -> str:
   respon = chain.invoke(question)
   return respon.content







