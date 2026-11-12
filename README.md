
# 📚 AI-Powered Document Intelligence Agent

An AI-powered document assistant that helps users upload, understand, summarize, compare and ask questions about multiple documents.

The application uses Llama 3.2, Retrieval-Augmented Generation (RAG), FAISS vector search and OCR to extract meaningful information from documents.

## 🚀 Features

- 📂 Multiple Document Upload
- 📖 Text Extraction from PDF, DOCX, TXT and PPTX
- 🖼️ OCR Support for Scanned PDFs and Images
- ✂️ Intelligent Text Chunking
- 🔢 Text Embeddings Generation
- 🗄️ FAISS Vector Database
- 🤖 AI-Powered Question Answering
- 📝 Short and Detailed Document Summaries
- 📌 Important Points Extraction
- 📊 Multiple Document Comparison
- ✅ Actionable Checklist Generation
- 📚 Source References and Page Numbers

## 🛠️ Tech Stack

**Frontend:** Streamlit

**Programming Language:** Python

**AI Model:** Ollama - Llama 3.2

**Vector Database:** FAISS

**Embeddings:** Sentence Transformers

**OCR:** Tesseract OCR and Pytesseract

**Document Processing:** PyMuPDF, python-docx, python-pptx

**Architecture:** Retrieval-Augmented Generation (RAG)

## 📁 Project Structure

```text
AI-Document-Intelligence-Agent/
│
├── app.py
├── requirements.txt
├── .gitignore
│
└── modules/
    ├── ai_agent.py
    ├── checklist.py
    ├── comparator.py
    ├── document_loader.py
    ├── embeddings.py
    ├── ocr_processor.py
    ├── retriever.py
    ├── summarizer.py
    ├── text_processor.py
    └── vector_database.py
```

## ⚙️ Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/stuti-kumbhare/AI-Document-Intelligence-Agent.git
```

### 2. Open the Project Folder

```bash
cd AI-Document-Intelligence-Agent
```

### 3. Create Virtual Environment

```bash
python -m venv venv
```

### 4. Activate Virtual Environment

For Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### 5. Install Dependencies

```bash
pip install -r requirements.txt
```

### 6. Install Ollama

Install Ollama and download the Llama 3.2 model:

```bash
ollama pull llama3.2
```

Make sure Ollama is running before starting the application.

### 7. Install Tesseract OCR

Install Tesseract OCR for Windows.

Default installation path:

```text
C:\Program Files\Tesseract-OCR
```

### 8. Run the Application

```bash
python -m streamlit run app.py
```

Open the Local URL displayed in your terminal.

## 💡 How It Works

1. Upload one or more documents.
2. Extract text using document processing and OCR.
3. Split extracted text into smaller chunks.
4. Generate vector embeddings.
5. Store embeddings in the FAISS vector database.
6. Retrieve relevant document sections based on user questions.
7. Generate contextual answers using Llama 3.2.

## 🎯 Project Objective

The goal of this project is to simplify document understanding through AI by providing quick answers, meaningful summaries, document comparisons and actionable checklists.

## 👩‍💻 Developer

**Stuti Kumbhare**

Artificial Intelligence and Machine Learning Student

GitHub: [stuti-kumbhare](https://github.com/stuti-kumbhare)

---

⭐ If you find this project useful, consider giving the repository a star!
