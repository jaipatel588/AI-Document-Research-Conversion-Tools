# 📚 AI Document Research & Conversion

AI Document Research & Conversion is a full-stack web application that allows users to upload and analyze multiple documents, extract key themes, and interact with document data using natural language queries. It uses modern AI techniques like LLMs, document embeddings, and OCR to convert raw files into meaningful insights and summaries. Tools aalso Document Conversion upload document any format convert to another format Tools

---

## 🚀 Key Features Tools

- 📄 Upload multiple documents (PDF, DOCX, Images)
- 🔍 AI-powered **theme identification**
- 💬 Ask questions about document content (Q&A)
- 🧾 Generate clean summaries from messy text
- 🖼 OCR support for scanned PDFs/images
- 🌐 Web-based UI with seamless UX
- 🧠 OpenAI integration for advanced document analysis
- ⚙️ Modular backend using FastAPI/Openai key uses with online + offeline (Sentence Transformer + Billing Quutos openai key for AI Summary) 

---

## 🛠 Tech Stack

### Frontend:
- React.js + Vite
- Chakra UI
- Run Process Backend then frontend run
- cd frontend
- npm run dev

### Backend:
- FastAPI (Python)
- Langchain or OpenAI API for document LLMs
- OCR with Tesseract (optional)
- Vector DB (FAISS / Chroma / Weaviate)
- Backend run cd backend
- then venv\Scripts\activate
- then uvicron app.main:app --reload

### DevOps:
- Uvicorn run setup
- GitHub for version control
- Optional: Render, Railway, or VPS for deployment