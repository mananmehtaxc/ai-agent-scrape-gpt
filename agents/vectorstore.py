import os
from langchain_community.vectorstores import FAISS
from langchain.schema.embeddings import Embeddings
from langchain.docstore.document import Document
from langchain.text_splitter import CharacterTextSplitter

VSTORE_DIR = "./data/faiss_store"

def create_vectorstore(chunks, embedding_model: Embeddings):
    splitter = CharacterTextSplitter(chunk_size=512, chunk_overlap=100)
    docs = [Document(page_content=c) for c in chunks]
    split_docs = splitter.split_documents(docs)
    vectorstore = FAISS.from_documents(split_docs, embedding_model)
    vectorstore.save_local(VSTORE_DIR)
    return vectorstore

def load_vectorstore(embedding_model: Embeddings):
    return FAISS.load_local(VSTORE_DIR, embedding_model, allow_dangerous_deserialization=True)