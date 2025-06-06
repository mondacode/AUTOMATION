# 🧠 Fullstack RAG Automation System

This is a full-stack Retrieval-Augmented Generation (RAG) system using:

- **Next.js** for frontend and backend
- **Tailwind CSS + ShadCN** for beautiful UI
- **LangChain + OpenAI + FAISS** for vector search and AI response
- **FAISS index** support for `.txt`, `.odt`, and `.epub` documents

## 📁 Project Structure

- `/app/page.tsx`: Frontend UI with Tailwind + ShadCN
- `/pages/api/query.ts`: API route to handle queries
- `/faiss_index`: Directory to store your vector index (not included)
- `/docs`: Place your source documents here

## 🚀 Getting Started

1. Clone the repo
2. Run `npm install`
3. Add your `.env` file with `OPENAI_API_KEY`
4. Run `npm run dev`

## 🧪 Build FAISS Index

Use the Python utilities (`build_faiss_index.py`) provided in the other automation package to generate `faiss_index/`.

## 🧠 Ask Questions

The frontend sends a query → retrieves docs from FAISS → generates GPT-4 answer.
