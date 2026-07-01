from langchain_community.document_loaders import DirectoryLoader, PyMuPDFLoader
# loads all the data from a file/folder/directory

loader = DirectoryLoader(
    path='books',
    glob='*.pdf',
    loader_cls=PyMuPDFLoader
)

docs = loader.load()
print(docs[0])
print(len(docs))

# lazy load dont load all the file all at once in the memory. it uses generator and load one file at a time in the memory
# good when there is large amount of data
docs_1 = loader.lazy_load()
print(docs[0])