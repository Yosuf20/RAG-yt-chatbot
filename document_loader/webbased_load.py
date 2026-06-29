from langchain_community.document_loaders import WebBaseLoader
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv

load_dotenv()

url = "https://en.wikipedia.org/wiki/Website"

loader = WebBaseLoader(url)
docs = loader.load()

print(len(docs))

model = ChatGroq(
    model="llama-3.3-70b-versatile"
)

promt = PromptTemplate(
    template="Answer the following question \n {question} from the following text -\n {text}",
    input_variables=["question","text"]
)

parser = StrOutputParser()

chain = promt | model | parser

print(chain.invoke({"question":'tell me about the history of website', 'text' : docs[0].page_content}))


