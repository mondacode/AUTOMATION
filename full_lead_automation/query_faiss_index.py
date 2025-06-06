import os
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI

def query_faiss_index(query: str, index_path: str = "./faiss_index", k: int = 3):
    # Load FAISS index and embeddings
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.load_local(index_path, embeddings)

    # Retrieve top-k matching chunks
    docs = vectorstore.similarity_search(query, k=k)
    context = "\n".join([doc.page_content for doc in docs])

    # Construct prompt for GPT
    prompt = f"Use the context below to answer the question.\n\nContext:\n{context}\n\nQuestion: {query}\nAnswer:"

    # Query GPT
    llm = ChatOpenAI(model_name="gpt-4")
    response = llm.predict(prompt)

    return response

if __name__ == "__main__":
    user_query = input("Enter your query: ")
    result = query_faiss_index(user_query)
    print("\nAnswer:\n", result)
