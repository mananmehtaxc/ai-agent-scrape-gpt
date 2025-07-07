import streamlit as st
from rag_graph import build_graph

st.set_page_config(page_title="ScrapeGPT", layout="wide")
st.title("🌐 ScrapeGPT — Chat with Web Pages")

# Inputs for API key and loading assistant
api_key = st.text_input("🔑 Enter your Google API Key", type="password")
load_button = st.button("🔄 Load Assistant")

# Initialize session state
if "assistant_loaded" not in st.session_state:
    st.session_state.assistant_loaded = False
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "chat_ready" not in st.session_state:
    st.session_state.chat_ready = False
if "current_url" not in st.session_state:
    st.session_state.current_url = None
if "summary" not in st.session_state:
    st.session_state.summary = ""

# Load assistant
if load_button:
    if not api_key:
        st.error("Please enter your API key.")
    else:
        st.session_state.api_key = api_key
        st.session_state.assistant_loaded = True

if not st.session_state.assistant_loaded:
    st.info("Enter your API key and click 'Load Assistant' to begin.")
    st.stop()

# Load RAG graph
graph = build_graph(st.session_state.api_key)

# Input for scraping a URL
url = st.text_input("🔗 Paste URL to scrape")

if st.button("Scrape and Summarize"):
    if not url.strip():
        st.error("Please enter a valid URL.")
    else:
        with st.spinner("Scraping and summarizing..."):
            try:
                cleaned_url = url.strip()
                state = {
                    "url": cleaned_url,
                    "query": "Summarize this page."
                }
                result = graph.invoke(state)
                st.session_state.summary = result.get("summary", "No summary generated.")
                st.session_state.current_url = cleaned_url
                st.session_state.chat_history = []  # Reset chat
                st.session_state.chat_ready = True
            except Exception as e:
                st.error(f"Error: {e}")
                st.session_state.chat_ready = False

# Show summary and chat input if ready
if st.session_state.chat_ready:
    st.subheader("🧠 Summary")
    st.write(st.session_state.summary)

    st.divider()
    st.subheader("💬 Ask a question")

    query = st.text_input("Type your question")

    if st.button("Ask"):
        if not query.strip():
            st.error("Please enter a question.")
        else:
            with st.spinner("Generating answer..."):
                try:
                    chat_state = {
                        "url": st.session_state.current_url,
                        "query": query.strip()
                    }
                    result = graph.invoke(chat_state)
                    response = result.get("response", "No response generated.")
                    st.session_state.chat_history.append(("user", query.strip()))
                    st.session_state.chat_history.append(("assistant", response))
                except Exception as e:
                    st.error(f"Error: {e}")

    for role, message in st.session_state.chat_history:
        st.markdown(f"**{role.title()}:** {message}")
