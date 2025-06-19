from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
index_path = "index"  # Assuming your folder is named `index/` with `index.faiss` and `index.pkl` inside

def get_retriever(k=5):
    db = FAISS.load_local(index_path, embedding_model, allow_dangerous_deserialization=True)
    return db.as_retriever(search_kwargs={"k": k})
