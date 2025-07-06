## 🚀 Project Name: **AI Agent ScrapeGPT**

*A Chat-Aware RAG Agent Built from URLs Using Google Gemini Model*

---
# Clone and enter project
git clone <repo-url>
cd <repo-folder>

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Run the project
python main.py

    ## This project uses streamlit run streamlit
    streamlit run main.py

# Deactivate when done
deactivate

# Freeze requirements.txt after installing new package
pip freeze > requirements.txt
---

### ✅ Components Overview

**1. Web Scraper**

* Scrape text from input URL
* Clean and preprocess HTML (remove ads, nav bars, etc.)
* Tools: `BeautifulSoup`, `requests`, or `Playwright` (for JS-heavy pages)

**2. Text Chunking and Embeddings**

* Split text into manageable chunks (e.g. 500 tokens)
* Create vector embeddings for each chunk
* Tools: Google Gemini Embeddings

**3. Vector Store (Knowledge Base)**

* Store embeddings to retrieve relevant chunks later
* Tools: `FAISS` (local, in-memory or disk-based), fully open-source

**4. RAG Pipeline**

* On user question, convert to embedding
* Retrieve top-k similar chunks from FAISS
* Feed them + question to a Gemini LLM
* Tools: `Transformers` + `Accelerate` or `Text Generation Inference` from Hugging Face

**5. Memory & Chat Features**

* Store chat history in context for conversational memory
* Long-term memory (optional): Save important Q/As
* Tools: `LangChain` (optional with Hugging Face), or custom Python memory store

---

### 🧠 Simple Tech Stack Example

| Component       | Tool/Lib                                        |
| --------------- | ----------------------------------------------- |
| Scraper         | `BeautifulSoup`, `Playwright`                   |
| Preprocessor    | `NLTK`, `re`, `tiktoken` (for chunking)         |
| Embedding Model | `sentence-transformers` on Gemini Embed         |
| Vector DB       | `FAISS`                                         |
| RAG Framework   | Custom or `LangChain` (Hugging Face compatible) |
| Chat Memory     | Local buffer, `LangChain` memory (optional)     |
| Backend         | `FastAPI`, `Flask`                              |
| UI (optional)   | `Streamlit`, `Gradio`, `Next.js`                |

---

### 🛠 Example Flow

1. **User Input:** Enters URL →
2. **Scraper:** Extracts main text →
3. **Preprocess + Chunk:** Text cleaning, split into chunks →
4. **Embed + Store:** Use `all-MiniLM-L6-v2` → store vectors in `FAISS` →
5. **Query:** User asks a question →
6. **Retrieve:** Get top-k similar chunks from FAISS →
7. **Generate:** Feed context + question →
8. **Respond:** Generate response with optional chat memory

---

### 🔁 Optional Enhancements

* Periodically re-scrape dynamic URLs (RSS, API support)
* Summarize documents using `bart-large-cnn`
* Enable PDF/YouTube/blog support for broader KB
* Chat profiles using lightweight DBs like SQLite or TinyDB

---

### File Stucture
ai-agent-scrape-gpt/
├── agents/
│   ├── rag_graph.py            # LangGraph node and edge logic
│   └── memory.py               # Memory buffer or vector memory
├── llm/
│   ├── gemini_wrapper.py       # Gemini API call handler
│   └── embedder.py             # Embedding function (Gemini or fallback)
├── html_scraper.py             # URL scraping and preprocessing logic
├── vectorstore/
│   └── store.py                # FAISS/Chroma setup and retrieval
├── main.py                     # FastAPI or Streamlit frontend
├── faiss_index                 # FAISS index files
├── requirements.txt
└── README.md

---
###  LangGraph Node Design

| Node Name          | Function                                       |
| ------------------ | ---------------------------------------------- |
| `scrape_node`      | Scrape and clean URL contents                  |
| `chunk_embed_node` | Chunk + Embed + Store in FAISS                 |
| `retrieve_node`    | Retrieve top-k chunks from FAISS               |
| `generate_node`    | Call Gemini with retrieved context             |
| `memory_node`      | Track prior conversation (optional state save) |
| `chat_node`        | Format + return final response                 |
