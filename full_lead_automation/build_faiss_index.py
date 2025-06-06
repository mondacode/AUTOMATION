import os
import faiss
import numpy as np
from typing import List, Dict
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.document_loaders import TextLoader, UnstructuredODTLoader, UnstructuredEPubLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

def load_documents_from_folder(folder_path: str) -> List[str]:
    documents = []
    for file in os.listdir(folder_path):
        full_path = os.path.join(folder_path, file)
        if file.endswith(".txt"):
            loader = TextLoader(full_path)
        elif file.endswith(".odt"):
            loader = UnstructuredODTLoader(full_path)
        elif file.endswith(".epub"):
            loader = UnstructuredEPubLoader(full_path)
        else:
            continue
        documents.extend(loader.load())
    return documents

def split_and_embed_documents(documents: List[str]) -> FAISS:
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_documents(documents)
    embeddings = OpenAIEmbeddings()
    return FAISS.from_documents(chunks, embeddings)

def build_faiss_index(input_folder: str, output_folder: str):
    documents = load_documents_from_folder(input_folder)
    if not documents:
        print("No documents loaded.")
        return
    print(f"Loaded {len(documents)} documents.")
    vectorstore = split_and_embed_documents(documents)
    vectorstore.save_local(output_folder)
    print(f"FAISS index saved to {output_folder}")

if __name__ == "__main__":
    input_dir = "./docs"
    output_dir = "./faiss_index"
    build_faiss_index(input_dir, output_dir)
