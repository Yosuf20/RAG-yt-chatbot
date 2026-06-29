from langchain_community.document_loaders import CSVLoader

file = CSVLoader("filepath.csv")

load = file.lazy_load()
print(load[0])
