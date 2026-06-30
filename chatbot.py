
# !pip install langchain faiss-cpu tiktoken langchain_huggingface langchain_community langchain-core -q youtube-transcript-api python-dotenv langchain_groq

from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.prompts import PromptTemplate
from youtube_transcript_api import YouTubeTranscriptApi
from langchain_core.runnables import RunnableParallel, RunnableLambda, RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
from langchain_community.vectorstores import FAISS
import os
from dotenv import load_dotenv
load_dotenv()


url = "https://www.youtube.com/watch?v=4b7fKbIPHPA"


def vid_id(url : str) -> str:
    video_id = url.split("=")[1].split("&")[0]
    return video_id

try:
  ytt_api = YouTubeTranscriptApi()

  transcript_list = ytt_api.fetch(
      video_id = vid_id(url),
      languages=['en']
      )
  transcript = " ".join(chunk.text for chunk in transcript_list)
except:
  print("No caption available")



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

def format_docs(content):
  context_text = "\n\n".join(doc.page_content for doc in content)
  return context_text

prompt = PromptTemplate(
    template="""
    You are a helpfull yt video chatbot
    Answer only from the provided transcript context
    If the context is insufficeint then simply say i dont know

    {context}
    Question: {question}
    """,
    input_variables=['context', 'question']
)

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY")
)

parallel_chain = RunnableParallel({
    'context' : retriever | RunnableLambda(format_docs),
    'question' : RunnablePassthrough()
})

parser = StrOutputParser()

chain = parallel_chain | prompt | llm | parser

print(chain.invoke('On which they are currently working'))

