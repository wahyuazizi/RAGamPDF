# **RAGamPDF Documentation** 📄➡️🤖

A simple RAG (Retrieval-Augmented Generation) system that lets you chat with your PDFs using Ollama models and Streamlit.

## **Project Overview**
- **What it does**: Upload a PDF, ask questions, get answers based on the document.
- **Tech Stack**: 
  - Ollama (for LLMs & embeddings)
  - Streamlit (web interface)
  - FAISS (vector storage)
  - PyMuPDF (PDF processing)

## **Prerequisites**
- Python 3.11+
- Ollama installed & running ([install guide](https://ollama.ai/download))
- At least one Ollama model (e.g., `llama3`)

## **Quick Setup** 🚀

### 1. Clone the repo
```bash
git clone https://github.com/yourusername/RAGamPDF.git
cd RAGamPDF
```

### 2. Set up environment
```bash
# Create Python env (using pyenv)
pyenv install 3.11.8
pyenv local 3.11.8

# Install dependencies
poetry install
```

### 3. Prepare Ollama
```bash
# Download a model (example). choose model you want
ollama pull llama3
```

## **Configuration** ⚙️
Create a `.env` file in project root:
```ini
OLLAMA_HOST=http://localhost:11434  # Default Ollama URL
DEFAULT_MODEL=llama3                # Change if you prefer other models
```

## **How to Run** ▶️

### **Option 1: Local Development**
```bash
# Start Ollama in one terminal
ollama serve

# In another terminal:
poetry run streamlit run frontend/app.py
```

<!-- ### **Option 2: Docker**
```bash
docker build -t ragampdf .
docker run -p 8501:8501 ragampdf
``` -->
Then visit `http://localhost:8501`

## **Using the App** 🖥️
1. Open `http://localhost:8501` in your browser
2. Upload a PDF file
3. Wait for processing (you'll see a success message)
4. Ask questions in the chat box!
