import os
from typing import List, Dict
from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
import numpy as np

def load_and_embed_documents(folder_path: str) -> List[Dict]:
    """
    Loads documents from the specified folder, splits them into chunks,
    embeds them using OpenAI, and returns vectorized documents.

    Returns:
        List of dicts with keys: 'text', 'vector'
    """
    embeddings = OpenAIEmbeddings()
    all_chunks = []

    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            loader = TextLoader(os.path.join(folder_path, filename))
            documents = loader.load()
            splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
            chunks = splitter.split_documents(documents)
            all_chunks.extend(chunks)

    embedded_docs = []
    for chunk in all_chunks:
        vector = embeddings.embed_query(chunk.page_content)
        embedded_docs.append({
            "text": chunk.page_content,
            "vector": np.array(vector, dtype='float32')
        })

    return embedded_docs
