from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
import os

embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
index_path = "index"  

def get_retriever(k=5):
    try:
        if os.path.exists(index_path):
            db = FAISS.load_local(index_path, embedding_model, allow_dangerous_deserialization=True)
            return db.as_retriever(search_kwargs={"k": k})
        else:
            print(f"Warning: Index path {index_path} does not exist. Creating empty retriever.")
            # Create an empty FAISS index as fallback
            from langchain.schema import Document
            empty_docs = [Document(page_content="", metadata={})]
            db = FAISS.from_documents(empty_docs, embedding_model)
            return db.as_retriever(search_kwargs={"k": k})
    except Exception as e:
        print(f"Error loading vector store: {e}")
        # Return a simple retriever that returns empty results
        from langchain.schema import Document
        empty_docs = [Document(page_content="", metadata={})]
        db = FAISS.from_documents(empty_docs, embedding_model)
        return db.as_retriever(search_kwargs={"k": k})
