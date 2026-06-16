from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEndpointEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
import os

os.environ["HUGGINGFACEHUB_API_TOKEN"] = "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"
embedding = HuggingFaceEndpointEmbeddings(
    model = "BAAI/bge-small-en-v1.5",
)

def create_vector_store(text : str):
    splitter = RecursiveCharacterTextSplitter(chunk_size = 1000 , chunk_overlap = 200)
    chunks = splitter.create_documents([text])
    vector_store = FAISS.from_documents(chunks,embedding)
    return vector_store

def search_knowledge_base(vector_store , query : str , k : int = 10):
    results = vector_store.similarity_search(query,k=k)
    return "\n\n".join([doc.page_content for doc in results])