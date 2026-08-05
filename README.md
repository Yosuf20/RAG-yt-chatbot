# 🎬 RAG Chatbot

A locally running RAG (Retrieval Augmented Generation) chatbot that lets you chat with any YouTube video or PDF document — completely offline using Ollama and HuggingFace embeddings.

---

## ✨ Features

- 🎥 Chat with any YouTube video using its transcript
- 📄 Chat with PDF documents
- 🌐 Auto-translates non-English transcripts to English
- 🔍 Hybrid search (MMR + BM25) for better retrieval
- 🦙 Fully local LLM using Ollama (no API key needed)
- ⚡ Fast embeddings with HuggingFace `bge-small-en-v1.5`
- 🛡️ YouTube IP block bypass using `curl_cffi`
- 🐳 Docker support for containerized deployment

---

## 🛠️ Tech Stack

| Component | Tool |
|---|---|
| LLM | Ollama (Qwen3 4B) |
| Embeddings | HuggingFace `BAAI/bge-small-en-v1.5` |
| Vector Store | FAISS |
| Keyword Search | BM25 |
| Transcript Fetch | youtube-transcript-api + curl_cffi |
| Translation | deep-translator |
| PDF Loading | PyMuPDF |
| Framework | LangChain |
| UI | Streamlit |
| Monitoring | LangSmith |
| Containerization | Docker |

---

## 📋 Requirements

- Python 3.10+
- [Ollama](https://ollama.com) installed
- NVIDIA GPU recommended (works on CPU too)

---

## 🚀 Installation

**1. Clone the repository:**
```bash
git clone https://github.com/Yosuf20/RAG-yt-chatbot.git
cd RAG-yt-chatbot
```

**2. Create and activate virtual environment:**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

**3. Install dependencies:**
```bash
pip install -r requirements.txt
```

**4. Install and setup Ollama:**
```bash
# Download from https://ollama.com then pull the model
ollama pull qwen3:4b
```

**5. Create `.env` file:**
```bash
# .env
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=your_langsmith_key
LANGCHAIN_PROJECT=your_project_name
LANGCHAIN_ENDPOINT=https://api.smith.langchain.com
```

---

## ▶️ Running the App

Make sure Ollama is running, then:
```bash
streamlit run app.py
```

---

## 🐳 Docker Setup

Run the entire app including Ollama in containers — no manual installation needed.

**Requirements:**
- [Docker Desktop](https://docker.com) installed
- NVIDIA GPU with CUDA support (for GPU acceleration)

**1. Build and start all containers:**
```bash
docker compose up --build
```

**2. Pull the model inside the Ollama container (first time only):**
```bash
docker exec ollama ollama pull qwen3:4b
```

**3. Open the app:**
```
http://localhost:8501
```

**Useful Docker commands:**
```bash
docker compose up --build    # build and start
docker compose up -d         # run in background
docker compose down          # stop everything
docker compose logs -f       # view logs
docker system prune -a       # free up storage
```

> **Note:** First run downloads all images (~3-4GB). Every run after that works offline with no internet needed (except for YouTube transcript fetching).

**🧹 Cleaning up Docker storage:**
```bash
# stop and remove containers
docker compose down

# remove all unused images (frees ~3-4GB)
docker system prune -a

# remove volumes including downloaded models (frees ~2.5GB)
docker volume prune

# nuclear option - remove everything
docker system prune -a --volumes
```

> **Warning:** `docker volume prune` deletes the downloaded Qwen3 model — you'll need to pull it again with `docker exec ollama ollama pull qwen3:4b`

---

## 📊 Evaluation

**LangSmith** is integrated for full pipeline observability. Every query is traced end-to-end, providing visibility into:

- Retrieval time (Hybrid BM25 + MMR search)
- Prompt formatting time
- LLM generation time (Qwen3 4B via Ollama)
- Total end-to-end response time

---

## 💡 How It Works

```
YouTube URL / PDF
      ↓
Fetch transcript / Extract text
      ↓
Translate to English (if needed)
      ↓
Split into chunks (500 tokens, 100 overlap)
      ↓
Embed with HuggingFace (bge-small-en-v1.5)
      ↓
Store in FAISS vector store
      ↓
User asks question
      ↓
Hybrid retrieval (MMR + BM25)
      ↓
Send context + question to Qwen3 4B (Ollama)
      ↓
Stream response to user
```

---

## ⚙️ Configuration

You can tweak the model settings in `chatbot.py`:

```python
def get_llm():
    return ChatOllama(
        model="qwen3:4b",    # change model here
        temperature=0.7,     # 0=focused, 1=creative
        think=False,         # disable thinking mode for speed
        num_ctx=2048,        # context window size
        repeat_penalty=1.1   # reduce repetition
    )
```

---

## 🔧 Troubleshooting

**YouTube IP blocked:**
```
YouTube blocks cloud/VPN IPs. Solutions:
- Wait 30-60 minutes for the block to lift
- Use a residential IP
- Export YouTube cookies and pass them to the API
```

**Ollama not recognized in terminal:**
```bash
# Windows - use full path
"C:\Users\YourName\AppData\Local\Programs\Ollama\ollama.exe" pull qwen3:4b

# Or add to PATH via Environment Variables
```

**Slow responses:**
```
- Ensure Ollama is using GPU (check nvidia-smi)
- Reduce num_ctx to 2048
- Set think=False
- Close other heavy applications to free RAM
```

**Docker GPU not working:**
```bash
# verify NVIDIA container toolkit is installed
nvidia-smi
docker run --gpus all nvidia/cuda:11.0-base nvidia-smi
```

---

## 📁 Project Structure

```
RAG-yt-chatbot/
├── app.py                # Streamlit UI
├── chatbot.py            # RAG pipeline
├── Dockerfile            # Docker image config
├── docker-compose.yml    # Multi-container setup
├── requirements.txt      # Python dependencies
├── .env                  # API keys (never commit this)
├── .gitignore
└── README.md
```

---

## 🙏 Acknowledgements

- [LangChain](https://langchain.com)
- [Ollama](https://ollama.com)
- [youtube-transcript-api](https://github.com/jdepoix/youtube-transcript-api)
- [HuggingFace](https://huggingface.co)
- [LangSmith](https://smith.langchain.com)