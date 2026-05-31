# 🏥 Healthcare AI — Smart Healthcare Companion

An AI-powered RAG chatbot that answers healthcare questions by reading PDF documents. Built with LangChain, ChromaDB, Flask, and Groq's free Llama 3.1 API.

## 🚀 Live Demo

👉 **[Try Healthcare AI Live](https://fardinannoy-healthcare-ai.hf.space)**

## ✨ Features

- **RAG Pipeline** — Loads PDFs, splits into chunks, generates vector embeddings
- **ChromaDB Vector Database** — Local, free, zero cloud costs
- **Conversational Memory** — Remembers chat context across messages
- **Professional UI** — Sidebar with quick topics, auto-expanding input, timestamps
- **Free to Run** — Uses Groq's free API + HuggingFace embeddings

## 🛠️ Tech Stack

- Python, Flask
- LangChain, ChromaDB
- HuggingFace Embeddings (all-MiniLM-L6-v2)
- Groq API (Llama 3.1)
- HTML/CSS/JavaScript

## 📦 Setup

1. Clone the repo
```bash
git clone https://github.com/FardinAnnoy27/Healthcare-AI.git
cd Healthcare-AI
```

2. Create virtual environment
```bash
python -m venv venv
.\venv\Scripts\Activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Add your Groq API key in a `.env` file
```
GROQ_API_KEY=your_key_here
```

5. Add PDF files to `data/` folder

6. Build the vector database
```bash
python store_index.py
```

7. Run the app
```bash
python app.py
```

## 🌐 Deployment

Deployed on [Hugging Face Spaces](https://huggingface.co/spaces/FardinAnnoy/Healthcare-ai) using Docker.

## 👨‍💻 Author

**Fardin** — Built as part of NextWork AI learning journey.
