from langchain_openai import ChatOpenAI
from langchain_community.document_loaders import TextLoader
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv #it loads secrete kkeys from .env to my the current file
from langchain_groq import ChatGroq

load_dotenv()

prompt = {}

model = ChatGroq(model='llama-3.3-70b-versatile')

prompt = PromptTemplate(
    template="Write a summary of the poem in 5 lines -\n {poem}",
    input_variables=['poem']
)

parser = StrOutputParser()

loader = TextLoader('football_poem.txt')

docs = loader.load()

chain = prompt | model | parser

print(chain.invoke({'poem' : docs[0].page_content}))

print
