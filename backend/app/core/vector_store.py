from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
import os
import pickle
import logging

logger = logging.getLogger(__name__)

# Lazy loading for embedding model to reduce initial memory usage
_embedding_model = None

def get_embedding_model():
    global _embedding_model
    if _embedding_model is None:
        try:
            _embedding_model = HuggingFaceEmbeddings(
                model_name="sentence-transformers/paraphrase-MiniLM-L3-v2",
                model_kwargs={'device': 'cpu'},
                encode_kwargs={'normalize_embeddings': True}
            )
        except:
            _embedding_model = HuggingFaceEmbeddings(
                model_name="sentence-transformers/all-MiniLM-L6-v2",
                model_kwargs={'device': 'cpu'},
                encode_kwargs={'normalize_embeddings': True}
            )
    return _embedding_model

index_path = "index"  

def get_retriever(k=5):
    try:
        if os.path.exists(f"{index_path}/faiss.index") and os.path.exists(f"{index_path}/documents.pkl"):
            import faiss
            import numpy as np
            
            index = faiss.read_index(f"{index_path}/faiss.index")
            with open(f"{index_path}/documents.pkl", "rb") as f:
                documents = pickle.load(f)
            
            class CustomRetriever:
                def __init__(self, index, documents, k=5):
                    self.index = index
                    self.documents = documents
                    self.k = k
                
                def get_relevant_documents(self, query):
                    try:
                        # Load embedding model only when needed
                        embedding_model = get_embedding_model()
                        query_embedding = embedding_model.embed_query(query)
                        query_vector = np.array([query_embedding]).astype('float32')
                        scores, indices = self.index.search(query_vector, self.k)
                        
                        results = []
                        for idx in indices[0]:
                            if idx < len(self.documents):
                                doc = self.documents[idx]
                                try:
                                    with open(doc.metadata['chunk_path'], 'r', encoding='utf-8') as f:
                                        doc.page_content = f.read()
                                    results.append(doc)
                                except:
                                    pass
                        return results
                    except:
                        return []
                
                def as_retriever(self, search_kwargs=None):
                    if search_kwargs and 'k' in search_kwargs:
                        self.k = search_kwargs['k']
                    return self
            
            return CustomRetriever(index, documents, k).as_retriever(search_kwargs={"k": k})
        else:
            from langchain.schema import Document
            empty_docs = [Document(page_content="", metadata={})]
            embedding_model = get_embedding_model()
            db = FAISS.from_documents(empty_docs, embedding_model)
            return db.as_retriever(search_kwargs={"k": k})
    except:
        from langchain.schema import Document
        empty_docs = [Document(page_content="", metadata={})]
        embedding_model = get_embedding_model()
        db = FAISS.from_documents(empty_docs, embedding_model)
        return db.as_retriever(search_kwargs={"k": k})
