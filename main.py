import streamlit as st
from agents.rag_graph import build_graph
import os

st.set_page_config(page_title="Customer Support Agent", page_icon="🔗")
st.title("🔍🔗 AI Agent Scrape GPT – Powered by Gemini")

# Set and Load Gimini API Key
gemini_api_key = st.text_input("🔑 Enter your Google API Key", type="password")
load_apikey_button = st.button("🔄 Load API Key")

# Store init state
if "assistant_loaded" not in st.session_state:
    st.session_state.assistant_loaded = False

# Load assistant after button is clicked
if load_apikey_button:
    if not gemini_api_key:
        st.error("Please enter your API key before loading the assistant.")
        st.stop()
    # os.environ["GOOGLE_API_KEY"] = api_key
    st.session_state.assistant_loaded = True

# Prevent loading before API key is set
if not st.session_state.assistant_loaded:
    st.info("Enter your API key and click 'Load Assistant' to begin.")
    st.stop()

url = st.text_input("🌐 Enter URL to scrape", placeholder="https://example.com")
query = st.text_input("❓ Ask a question about the content")

if st.button("🚀 Start Scraping and Querying"):
    if not url:
        st.error("Please enter a URL to scrape.")
    elif not query:
        st.error("Please enter a question to ask.")
    else:
        with st.spinner("🔄 Scraping and processing..."):
            try:
                graph = build_graph(gemini_api_key)
                state = {"url": url, "query": query}
                result = graph.invoke(state)
                st.success("✅ Successfully processed!")
                st.write("🔍 Context:", result["context"])
                st.write("💬 Response:", result["response"])
            except Exception as e:
                st.error(f"❌ Error: {e}")


