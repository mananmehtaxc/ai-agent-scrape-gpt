from langgraph.graph import StateGraph, START, END
from langchain_google_genai import GoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from agents.vectorstore import create_vectorstore, load_vectorstore
from utils.html_scraper import scrape_html
from langchain.memory import ConversationBufferMemory

class RAGState(dict):
    url: str
    query: str
    scraped_text: str
    chunks: list
    context: str
    response: str
    summary: str

def build_graph(api_key: str):
    llm = GoogleGenerativeAI(model="gemini-2.0-flash", google_api_key=api_key)
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=api_key)
    memory = ConversationBufferMemory(return_messages=True)

    def scrape_node(state):
        state["scraped_text"] = scrape_html(state["url"])
        return state

    def embed_node(state):
        chunks = state["scraped_text"].split("\n\n")
        state["chunks"] = chunks
        create_vectorstore(chunks, embeddings)
        return state

    def summarize_node(state):
        prompt = f"Summarize this web page:\n\n{state['scraped_text']}"
        state["summary"] = llm.invoke(prompt)
        return state

    def query_node(state):
        vectorstore = load_vectorstore(embeddings)
        results = vectorstore.similarity_search(state["query"], k=5)
        context = "\n".join([r.page_content for r in results])
        state["context"] = context
        return state

    def generate_node(state):
        prompt = f"""
        Use the following context to answer the question:

        Context:
        {state['context']}

        Question: {state['query']}
        """
        response = llm.invoke(prompt)
        memory.chat_memory.add_user_message(state["query"])
        memory.chat_memory.add_ai_message(response)
        state["response"] = response
        return state

    # Define graph
    graph = StateGraph(RAGState)
    graph.add_node("scrape", scrape_node)
    graph.add_node("embed", embed_node)
    graph.add_node("summarize", summarize_node)
    graph.add_node("query", query_node)
    graph.add_node("generate", generate_node)

    graph.add_edge(START, "scrape")
    graph.add_edge("scrape", "embed")
    graph.add_edge("embed", "summarize")
    graph.add_edge("summarize", "query")
    graph.add_edge("query", "generate")
    graph.add_edge("generate", END)

    return graph.compile()
