import faiss
import numpy as np
from openai import OpenAI
from typing import List

# Assume a simple in-memory FAISS index with dummy vectors and metadata
# In practice, this would be a persistent index and document store

dimension = 1536  # For OpenAI embeddings (text-embedding-ada-002)
index = faiss.IndexFlatL2(dimension)
documents = [
    {"id": 0, "text": "Acme Corp is a SaaS company focused on EU markets.", "vector": np.random.rand(dimension).astype('float32')},
    {"id": 1, "text": "They have raised Series B funding.", "vector": np.random.rand(dimension).astype('float32')},
]

# Build index
vectors = np.array([doc["vector"] for doc in documents])
index.add(vectors)

# Attach document metadata for lookup
doc_map = {i: doc["text"] for i, doc in enumerate(documents)}

# Embed a query and perform FAISS search
def perform_rag(query: str) -> str:
    openai = OpenAI()

    # Step 1: Embed query
    embedding_response = openai.embeddings.create(
        input=query,
        model="text-embedding-ada-002"
    )
    query_vec = np.array(embedding_response["data"][0]["embedding"]).astype("float32").reshape(1, -1)

    # Step 2: Search FAISS
    top_k = 2
    _, I = index.search(query_vec, top_k)

    # Step 3: Retrieve matching documents
    retrieved_docs = [doc_map[i] for i in I[0]]

    # Step 4: Construct prompt
    context = "\n".join(retrieved_docs)
    prompt = f"Use the context below to answer the question.\nContext: {context}\n\nQuestion: {query}\nAnswer:"

    # Step 5: Generate response
    completion = openai.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return completion["choices"][0]["message"]["content"]
