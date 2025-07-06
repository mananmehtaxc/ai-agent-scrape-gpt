from langchain_google_genai import GoogleGenerativeAIEmbeddings, GoogleGenerativeAI

# Initialize the LLM with the Gemini API key
def get_llm (gemini_api_key):
    return GoogleGenerativeAI(
        model="models/gemini-2.5-flash",
        gemini_api_key=gemini_api_key)


