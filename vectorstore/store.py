import faiss # This line imports the FAISS library, which is used for efficient similarity search and clustering of dense vectors.
import pickle # This line imports the pickle module, which is used for serializing and deserializing Python objects.
import os
from langchain.vectorstores.faiss import FAISS # This line imports the FAISS vector store implementation from LangChain, which is a library for building applications with language models.
from langchain.schema import Document # This line imports the Document class from LangChain, which represents a text document with metadata.


def create_vector_store(documents: list[str], embedding_model) -> FAISS:
    """
    Create a FAISS vector store from a list of documents.

    Args:
        documents (list[str]): A list of text documents to be embedded and stored.

    Returns:
        FAISS: An instance of the FAISS vector store containing the embedded documents.
    """
    docs = [Document(page_content=doc) for doc in documents]  # Convert each document string into a Document object.
    return FAISS.from_documents(docs, embedding_model)  # Create and return a FAISS vector store from the documents using the embedding model.

def save_vector_store(faiss_store, file_path: "data/faiss_index") -> None:
    os.makedirs (os.path.dirname(file_path), exist_ok=True)  # Ensure the directory exists.
    faiss_store.save_local(file_path)  # Save the FAISS vector store to the specified file path.

def load_vector_store(embedding_model,file_path: "data/faiss_index") -> FAISS:
    """
    Load a FAISS vector store from a file.

    Args:
        file_path (str): The path to the file containing the serialized FAISS vector store.

    Returns:
        FAISS: An instance of the FAISS vector store loaded from the file.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Vector store file not found: {file_path}")  # Raise an error if the file does not exist.
    
    return FAISS.load_local(file_path, embedding_model)  # Load and return the FAISS vector store from the specified file path.