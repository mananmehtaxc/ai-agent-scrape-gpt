from html_scraper import scrape_html
from llm.embedder import embed_text,get_embedding_model
from vectorstore.store import create_vector_store, save_vector_store, load_vector_store
from llm.gemini_wrapper import get_llm
from agents.memory import save_memory, get_memory

memory = get_memory()

def build_graph(google_gemini_api_key: str):
    llm = get_llm(google_gemini_api_key)
    embedding_model = get_embedding_model(google_gemini_api_key)

    def scrape_node (state):
        state["scraped_text"] = scrape_html(state["url"])
        if state["scraped_text"]:
            return state
        else:
            raise ValueError("Failed to scrape the URL. Please check the URL and try again.")

    def embed_node (state):
        chunks = state["scraped_text"].split("\n\n") # Split the text into chunks by paragraphs
        state["chunks"] = chunks
        vectorstore = create_vector_store(chunks, embedding_model)
        save_vector_store(vectorstore)
        return state

    def query_node (state):
        vectorstore = load_vector_store(embedding_model)
        results = vectorstore.similarity_search(state["query"], k=5)
        state["context"] = "\n".join([r.page_content for r in results])
        return state

    def generate_node (state):
        prompt = f"""
        You are a helpful AI assistant that scraps URL and provide summary from URL and ready to answer questions ask by users. Use the following context to answer the user's question.
        
        Context:
        {state["context"]}
        
        Question: {state["query"]}
        
        Answer:
        """
        messages = memory.chat_memory.messages
        messages.append({"role": "user", "content": state})
        response = llm.invoke(prompt)
        memory.chat_memory.messages.append({"role": "assistant", "content": response})
        save_memory(memory)
        state["response"] = response
        return state
    
    from langgraph.graph import StateGraph
    graph = StateGraph()
    # Define nodes
    scrape_node = graph.add_node("scrape", scrape_node)
    embed_node = graph.add_node("embed", embed_node)
    query_node = graph.add_node("query", query_node)
    generate_node = graph.add_node("generate", generate_node)
    
    graph.set_entry_point("scrape")
    graph.set_edge("scrape", "embed")
    graph.set_edge("embed", "query")
    graph.set_edge("query", "generate")
    graph.set_exit_point("generate")
    
    return graph.compile()

    
    