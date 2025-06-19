# DocuMind

DocuMind is a full-stack AI-powered document management and Q&A platform.
It allows users to securely upload documents, then ask natural language questions and get intelligent answers based on their content.

---

## Features

- **Secure Document Upload:** Upload PDFs, PowerPoints, CSVs, DOCX, and more.
- **AI-Powered Search & Q&A:** Ask questions in plain English and get answers with context.
- **User Authentication:** Register and log in to manage your own documents.
- **Modern UI:** Clean, responsive React frontend with beautiful design.
- **FastAPI Backend:** Robust, scalable Python backend with FastAPI.
- **Database Storage:** User and document data stored securely.
- **Extensible:** Built with modern frameworks and ready for further customization.

---

## Project Structure

```
doc_chat/
  ├── doc_chat_backend/   # FastAPI backend
  │   ├── app/            # Main backend app code
  │   ├── requirements.txt
  │   └── ...
  └── doc_chat_frontend/  # React frontend (Vite + TypeScript + Tailwind)
      ├── src/
      ├── package.json
      └── ...
```

---

## Getting Started

### Prerequisites

- Python 3.10+
- Node.js 18+
- npm

---

### 1. Backend Setup (FastAPI)

```bash
cd doc_chat_backend
pip install -r requirements.txt
```

#### Run the backend server:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

The backend will be available at [http://localhost:8000](http://localhost:8000).

---

### 2. Frontend Setup (React + Vite)

```bash
cd doc_chat_frontend
npm install
```

#### Run the frontend dev server:

```bash
npm run dev
```

The frontend will be available at [http://localhost:8080](http://localhost:8080).

---

## Usage

1. **Register** for a new account or log in.
2. **Upload** your documents (PDF, DOCX, PPTX, CSV, etc.).
3. **Ask questions** about your documents using natural language.
4. **Get instant answers** powered by AI, with context and citations.

---

## Tech Stack

- **Frontend:** React, TypeScript, Vite, Tailwind CSS, Radix UI, React Query
- **Backend:** FastAPI, SQLAlchemy, JWT Auth, LangChain, CrewAI, Elasticsearch, HuggingFace Transformers, unstructured.io
- **Database:** postgressql (default, can be changed)
- **Other:** Docker-ready, extensible for cloud deployment

---

## Customization

- To use a different database, set the `DATABASE_URL` in a `.env` file in `doc_chat_backend`.
- To use a different AI model or vector store, modify the backend's `embeddings.py` and related files.

---

## License

This project is for educational and demonstration purposes.

---

## Acknowledgements

- Built with [FastAPI](https://fastapi.tiangolo.com/), [React](https://react.dev/), [LangChain](https://www.langchain.com/), [CrewAI](https://crewai.com/), and [HuggingFace](https://huggingface.co/). 