# Mock RAG Module

This module (`mock_rag_api.py`) simulates a Retrieval-Augmented Generation (RAG) pipeline.

### How it works:
- Mimics embedding + vector store retrieval
- Provides a static but realistic context
- Returns a simulated GPT-style answer

### Usage:
Replace any real `perform_rag(query)` call with this mock during development or testing.
\n\n---\n\n# Real RAG Module (FAISS + OpenAI)

This module demonstrates an actual Retrieval-Augmented Generation (RAG) implementation using:

- FAISS for in-memory vector search
- OpenAI for embeddings and response generation

### Steps:
1. Embed the query with OpenAI
2. Use FAISS to find top matching vectors
3. Construct context and use GPT-4 for a final answer

This setup uses random vectors as placeholders. Replace them with real document vectors and texts in production.

\n\n---\n\n# Document Loader for FAISS + RAG

This utility (`document_loader.py`) loads `.txt` documents from a folder, splits them into chunks, and converts them to OpenAI embeddings.

### How to Use:

1. Place `.txt` files in a folder (e.g., `./docs/`)
2. Call `load_and_embed_documents('./docs/')`
3. Use returned vectors to populate FAISS

The returned list can be directly used to build your FAISS index.
