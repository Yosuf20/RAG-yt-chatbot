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

---

## 📋 Requirements

- Python 3.10+
- [Ollama](https://ollama.com) installed
- NVIDIA GPU recommended (works on CPU too)

---

## 🚀 Installation

**1. Clone the repository:**
```bash
git clone https://github.com/yourusername/youtube-rag-chatbot.git
cd youtube-rag-chatbot
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
GROQ_API_KEY=your_key_here   # optional, only if using Groq
```

---

## ▶️ Running the App

Make sure Ollama is running, then:
```bash
streamlit run app.py
```

---

Install all at once:
```bash
pip install -r requirements.txt
```

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
# Add to PATH or use full path
"C:\Users\YourName\AppData\Local\Programs\Ollama\ollama.exe" pull qwen3:4b
```

**Slow responses:**
```
- Ensure Ollama is using GPU (check nvidia-smi)
- Reduce num_ctx to 2048
- Set think=False
- Close other heavy applications to free RAM
```

---

## 📁 Project Structure

```
youtube-rag-chatbot/
├── app.py          # Streamlit UI
├── chatbot.py      # RAG pipeline
├── .env            # API keys (never commit this)
├── .gitignore
├── requirements.txt
└── README.md
```

---

## 🙏 Acknowledgements

- [LangChain](https://langchain.com)
- [Ollama](https://ollama.com)
- [youtube-transcript-api](https://github.com/jdepoix/youtube-transcript-api)
- [HuggingFace](https://huggingface.co)
