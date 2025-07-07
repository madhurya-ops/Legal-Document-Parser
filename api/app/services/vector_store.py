from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
import os
import pickle
import logging
import asyncio
from typing import List, Optional, Dict, Any

from ..core.config import get_settings

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

class VectorStoreService:
    """Service for managing vector embeddings and similarity search"""
    
    def __init__(self):
        self.embedding_model = None
        self.index_path = index_path
    
    def _get_embedding_model(self):
        """Get or initialize the embedding model"""
        if self.embedding_model is None:
            self.embedding_model = get_embedding_model()
        return self.embedding_model
    
    async def create_embeddings(self, texts: List[str], metadata: List[Dict] = None) -> List[List[float]]:
        """Create embeddings for a list of texts"""
        try:
            model = self._get_embedding_model()
            
            # Run in executor to avoid blocking
            loop = asyncio.get_event_loop()
            embeddings = await loop.run_in_executor(
                None, 
                lambda: model.embed_documents(texts)
            )
            
            return embeddings
        except Exception as e:
            logger.error(f"Error creating embeddings: {e}")
            return []
    
    async def store_documents(self, documents: List[Dict], collection_id: str = None) -> bool:
        """Store documents in vector database"""
        try:
            from langchain.schema import Document
            
            # Convert to LangChain documents
            docs = []
            for doc in documents:
                content = doc.get('content', '')
                metadata = doc.get('metadata', {})
                if collection_id:
                    metadata['collection_id'] = collection_id
                docs.append(Document(page_content=content, metadata=metadata))
            
            if not docs:
                return False
            
            # Create embeddings and store
            model = self._get_embedding_model()
            
            # Run in executor to avoid blocking
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(
                None,
                lambda: self._store_documents_sync(docs, model)
            )
            
            return True
        except Exception as e:
            logger.error(f"Error storing documents: {e}")
            return False
    
    def _store_documents_sync(self, docs, model):
        """Synchronous document storage"""
        try:
            if os.path.exists(f"{self.index_path}/faiss.index"):
                # Load existing index
                import faiss
                index = faiss.read_index(f"{self.index_path}/faiss.index")
                with open(f"{self.index_path}/documents.pkl", "rb") as f:
                    existing_docs = pickle.load(f)
                
                # Add new documents
                db = FAISS.from_documents(existing_docs + docs, model)
            else:
                # Create new index
                db = FAISS.from_documents(docs, model)
            
            # Save index
            if not os.path.exists(self.index_path):
                os.makedirs(self.index_path)
            
            db.save_local(self.index_path)
            logger.info(f"Stored {len(docs)} documents in vector index")
        except Exception as e:
            logger.error(f"Error in sync document storage: {e}")
            raise
    
    async def search_similar(self, query: str, k: int = 5, collection_id: str = None) -> List[Dict]:
        """Search for similar documents"""
        try:
            retriever = get_retriever(k=k)
            
            # Run in executor to avoid blocking
            loop = asyncio.get_event_loop()
            results = await loop.run_in_executor(
                None,
                lambda: retriever.get_relevant_documents(query)
            )
            
            # Filter by collection if specified
            if collection_id:
                results = [doc for doc in results if doc.metadata.get('collection_id') == collection_id]
            
            # Convert to dict format
            formatted_results = []
            for doc in results:
                formatted_results.append({
                    'content': doc.page_content,
                    'metadata': doc.metadata,
                    'score': 1.0  # FAISS doesn't return scores in this setup
                })
            
            return formatted_results
        except Exception as e:
            logger.error(f"Error searching similar documents: {e}")
            return []
    
    async def delete_collection(self, collection_id: str) -> bool:
        """Delete documents from a specific collection"""
        try:
            if not os.path.exists(f"{self.index_path}/documents.pkl"):
                return True  # Nothing to delete
            
            # Load existing documents
            with open(f"{self.index_path}/documents.pkl", "rb") as f:
                documents = pickle.load(f)
            
            # Filter out documents from the specified collection
            filtered_docs = [doc for doc in documents if doc.metadata.get('collection_id') != collection_id]
            
            if len(filtered_docs) != len(documents):
                # Recreate index with filtered documents
                if filtered_docs:
                    model = self._get_embedding_model()
                    loop = asyncio.get_event_loop()
                    await loop.run_in_executor(
                        None,
                        lambda: self._store_documents_sync(filtered_docs, model)
                    )
                else:
                    # Delete entire index if no documents left
                    if os.path.exists(f"{self.index_path}/faiss.index"):
                        os.remove(f"{self.index_path}/faiss.index")
                    if os.path.exists(f"{self.index_path}/documents.pkl"):
                        os.remove(f"{self.index_path}/documents.pkl")
                
                logger.info(f"Deleted collection {collection_id}")
            
            return True
        except Exception as e:
            logger.error(f"Error deleting collection: {e}")
            return False
    
    async def get_collection_stats(self, collection_id: str = None) -> Dict:
        """Get statistics about collections"""
        try:
            if not os.path.exists(f"{self.index_path}/documents.pkl"):
                return {"total_documents": 0, "collections": {}}
            
            with open(f"{self.index_path}/documents.pkl", "rb") as f:
                documents = pickle.load(f)
            
            if collection_id:
                # Stats for specific collection
                collection_docs = [doc for doc in documents if doc.metadata.get('collection_id') == collection_id]
                return {
                    "collection_id": collection_id,
                    "document_count": len(collection_docs),
                    "total_characters": sum(len(doc.page_content) for doc in collection_docs)
                }
            else:
                # Overall stats
                collections = {}
                for doc in documents:
                    cid = doc.metadata.get('collection_id', 'default')
                    if cid not in collections:
                        collections[cid] = {"count": 0, "characters": 0}
                    collections[cid]["count"] += 1
                    collections[cid]["characters"] += len(doc.page_content)
                
                return {
                    "total_documents": len(documents),
                    "collections": collections
                }
        except Exception as e:
            logger.error(f"Error getting collection stats: {e}")
            return {"total_documents": 0, "collections": {}}

# Service factory function to avoid module-level instantiation
def get_vector_store_service() -> VectorStoreService:
    """Get vector store service instance."""
    return VectorStoreService()

# For backward compatibility, create lazy-loaded instance
class _LazyVectorStoreService:
    _instance = None
    
    def __getattr__(self, name):
        if self._instance is None:
            self._instance = VectorStoreService()
        return getattr(self._instance, name)

# Create lazy instance for backward compatibility
vector_store_service = _LazyVectorStoreService()
