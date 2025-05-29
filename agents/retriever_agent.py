from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import TextLoader
from langchain_community.embeddings import SentenceTransformerEmbeddings

def initialize_retriever(doc_path="sample_data.txt"):
    loader = TextLoader(doc_path)
    documents = loader.load()

    embeddings = SentenceTransformerEmbeddings(model_name="/models/all-MiniLM-L6-v2")

    vector_store = FAISS.from_documents(documents, embeddings)
    return vector_store.as_retriever(search_kwargs={"k": 3})
