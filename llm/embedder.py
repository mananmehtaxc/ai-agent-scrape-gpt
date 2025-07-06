from langchain_google_genai import GoogleGenerativeAIEmbeddings, GoogleGenerativeAI


def get_embedding_model (gemini_api_key):
    return GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-exp-03-07", gemini_api_key=gemini_api_key)


def embed_text(text: list[str]) -> list:
    """    Embed a list of text documents using the Google Generative AI embedding model.   """
    return get_embedding_model().embed_documents(text)
    