<div align="center">

# 🧠 IntelliDocs AI

### Enterprise Retrieval-Augmented Generation (RAG) Platform for Intelligent Document Search & Question Answering

<p align="center">

<img src="https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python"/>

<img src="https://img.shields.io/badge/Streamlit-Web_App-red?style=for-the-badge&logo=streamlit"/>

<img src="https://img.shields.io/badge/Google-Gemini_AI-4285F4?style=for-the-badge&logo=google"/>

<img src="https://img.shields.io/badge/LangChain-RAG-green?style=for-the-badge"/>

<img src="https://img.shields.io/badge/ChromaDB-Vector_Database-orange?style=for-the-badge"/>

<img src="https://img.shields.io/badge/License-MIT-success?style=for-the-badge"/>

</p>

---

### 🚀 AI-Powered Enterprise Knowledge Assistant

Upload PDF documents, build a semantic knowledge base, retrieve relevant information using vector search, and generate context-aware answers with Google Gemini.

</div>

---

# ✨ Features

✅ Enterprise-inspired modern dashboard

✅ Upload PDF documents

✅ Automatic knowledge base generation

✅ Semantic chunking & embeddings

✅ Chroma Vector Database

✅ Context-aware Retrieval-Augmented Generation (RAG)

✅ Google Gemini integration

✅ AI-powered conversational interface

✅ Source chunk visualization

✅ Persistent local vector storage

✅ Responsive professional UI

---

# 🖥 Dashboard Preview

> Add screenshots here after uploading them.

```
assets/dashboard.png

assets/chat.png

assets/upload.png
```

---

# 🏗 System Architecture

```
                 PDF Documents
                       │
                       ▼
             Document Loader
                       │
                       ▼
              Text Chunking
                       │
                       ▼
         Gemini Embedding Model
                       │
                       ▼
                Chroma Vector DB
                       │
        Semantic Similarity Search
                       │
                       ▼
           Retrieved Context Chunks
                       │
                       ▼
             Gemini 2.5 Flash LLM
                       │
                       ▼
             Intelligent Response
```

---

# 📁 Project Structure

```text
IntelliDocs-AI
│
├── app.py
├── ingest.py
├── requirements.txt
├── .env
│
├── data/
│      sample.pdf
│
├── .chroma_db/
│
├── assets/
│      dashboard.png
│      upload.png
│      chat.png
│
└── README.md
```

---

# ⚙ Tech Stack

| Technology | Purpose |
|------------|----------|
| Python | Backend |
| Streamlit | Frontend |
| LangChain | RAG Pipeline |
| Google Gemini | Large Language Model |
| Gemini Embeddings | Text Embeddings |
| ChromaDB | Vector Database |
| PyPDF | PDF Processing |
| dotenv | Environment Variables |

---

# 🚀 Installation

Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/IntelliDocs-AI.git
```

Go inside the project

```bash
cd IntelliDocs-AI
```

Create virtual environment

```bash
python -m venv venv
```

Activate environment

Windows

```bash
venv\Scripts\activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

# 🔑 Environment Variables

Create a `.env` file

```env
GEMINI_API_KEY=YOUR_API_KEY
```

---

# ▶ Run the Application

```bash
streamlit run app.py
```

---

# 📚 How It Works

1. Upload a PDF document

2. Document is split into semantic chunks

3. Gemini Embedding Model converts chunks into vectors

4. ChromaDB stores vector embeddings

5. User submits a query

6. Semantic Search retrieves the most relevant chunks

7. Gemini generates an answer using retrieved context

8. Source chunks are displayed for transparency

---

# 💡 Key Capabilities

- Enterprise document search
- AI-powered knowledge retrieval
- Semantic similarity search
- Retrieval-Augmented Generation (RAG)
- Interactive conversational assistant
- Persistent knowledge base
- Professional dashboard

---

# 📈 Future Improvements

- Multi-document support

- Chat history persistence

- Authentication

- User workspaces

- Multiple vector databases

- Cloud deployment

- Citation highlighting

- OCR support

- Drag & Drop upload

- Multiple LLM providers

---

# 📸 Screenshots

| Dashboard | Upload | Chat |
|------------|---------|------|
| Add Screenshot | Add Screenshot | Add Screenshot |

---

# 👨‍💻 Developed By

**Hare Krishna**

Computer Science Undergraduate

AI • Machine Learning • Full Stack Development

---

# ⭐ If you found this project useful

Please consider giving the repository a ⭐

It motivates further development.

---

<div align="center">

Made with ❤️ using

**Python • Streamlit • LangChain • Gemini AI • ChromaDB**

</div>
