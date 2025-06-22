from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
import os
import pickle

# Use lighter embedding model
try:
    embedding_model = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={'device': 'cpu'},
        encode_kwargs={'normalize_embeddings': True}
    )
except Exception as e:
    print(f"Error loading embedding model: {e}")
    # Fallback to even lighter model
    embedding_model = HuggingFaceEmbeddings(
        model_name="sentence-transformers/paraphrase-MiniLM-L3-v2",
        model_kwargs={'device': 'cpu'},
        encode_kwargs={'normalize_embeddings': True}
    )

index_path = "index"  

def get_retriever(k=5):
    try:
        if os.path.exists(f"{index_path}/faiss.index") and os.path.exists(f"{index_path}/documents.pkl"):
            # Load the custom FAISS index
            import faiss
            import numpy as np
            
            # Load FAISS index
            index = faiss.read_index(f"{index_path}/faiss.index")
            
            # Load documents
            with open(f"{index_path}/documents.pkl", "rb") as f:
                documents = pickle.load(f)
            
            # Create a custom retriever
            class CustomRetriever:
                def __init__(self, index, documents, embedding_model, k=5):
                    self.index = index
                    self.documents = documents
                    self.embedding_model = embedding_model
                    self.k = k
                
                def get_relevant_documents(self, query):
                    try:
                        # Get query embedding
                        query_embedding = self.embedding_model.embed_query(query)
                        query_vector = np.array([query_embedding]).astype('float32')
                        
                        # Search
                        scores, indices = self.index.search(query_vector, self.k)
                        
                        # Return documents
                        results = []
                        for idx in indices[0]:
                            if idx < len(self.documents):
                                results.append(self.documents[idx])
                        
                        return results
                    except Exception as e:
                        print(f"Error in retrieval: {e}")
                        return []
                
                def as_retriever(self, search_kwargs=None):
                    if search_kwargs and 'k' in search_kwargs:
                        self.k = search_kwargs['k']
                    return self
            
            return CustomRetriever(index, documents, embedding_model, k).as_retriever(search_kwargs={"k": k})
            
        else:
            print(f"Warning: Index files not found. Creating empty retriever.")
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
