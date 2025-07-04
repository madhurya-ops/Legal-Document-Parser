from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.schema import Document
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
            logger.info("Loaded embedding model: paraphrase-MiniLM-L3-v2")
        except Exception as e:
            logger.warning(f"Failed to load paraphrase-MiniLM-L3-v2: {e}")
            try:
                _embedding_model = HuggingFaceEmbeddings(
                    model_name="sentence-transformers/all-MiniLM-L6-v2",
                    model_kwargs={'device': 'cpu'},
                    encode_kwargs={'normalize_embeddings': True}
                )
                logger.info("Loaded fallback embedding model: all-MiniLM-L6-v2")
            except Exception as e2:
                logger.error(f"Failed to load any embedding model: {e2}")
                raise e2
    return _embedding_model

index_path = "index"  

# Global variable to store the FAISS database
_global_db = None

def get_retriever(k=5):
    global _global_db
    try:
        embedding_model = get_embedding_model()
        
        # Try to load existing index first
        if _global_db is None:
            if os.path.exists(index_path) and os.path.exists(os.path.join(index_path, "index.faiss")):
                try:
                    logger.info("Loading existing FAISS index")
                    _global_db = FAISS.load_local(index_path, embedding_model, allow_dangerous_deserialization=True)
                    logger.info("Successfully loaded existing FAISS index")
                except Exception as e:
                    logger.warning(f"Failed to load existing index: {e}")
                    _global_db = None
            
            # If no existing index or failed to load, create new one
            if _global_db is None:
                logger.info("Creating new FAISS index with system message")
                empty_docs = [Document(page_content="Welcome to LegalDoc. Upload documents to get started. Please upload a document to analyze.", metadata={"source": "system"})]
                _global_db = FAISS.from_documents(empty_docs, embedding_model)
                
                # Save the new index
                if not os.path.exists(index_path):
                    os.makedirs(index_path)
                _global_db.save_local(index_path)
        
        return _global_db.as_retriever(search_kwargs={"k": k})
        
    except Exception as e:
        logger.error(f"Error initializing retriever: {e}")
        # Fallback to mock retriever
        class MockRetriever:
            def __init__(self, k=5):
                self.k = k
            
            def invoke(self, query):
                return [Document(page_content="Please upload a document first to get started with document analysis.", metadata={"source": "fallback"})]
        
        return MockRetriever(k)

async def add_documents_to_vector_store(text: str, file_path: str):
    """Add documents to the vector store by chunking the text"""
    global _global_db
    try:
        from langchain.text_splitter import RecursiveCharacterTextSplitter
        
        logger.info(f"Starting to add document to vector store: {file_path}")
        logger.info(f"Text length: {len(text)} characters")
        
        # Initialize text splitter
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            separators=["\n\n", "\n", ". ", "! ", "? ", " ", ""]
        )
        
        # Split text into chunks
        chunks = text_splitter.split_text(text)
        logger.info(f"Split text into {len(chunks)} chunks")
        
        # Create Document objects
        docs = []
        for i, chunk in enumerate(chunks):
            doc = Document(
                page_content=chunk,
                metadata={
                    "source": file_path,
                    "chunk": i,
                    "total_chunks": len(chunks)
                }
            )
            docs.append(doc)
            logger.info(f"Chunk {i}: {len(chunk)} chars, preview: {chunk[:100]}...")
        
        # Ensure we have an embedding model
        embedding_model = get_embedding_model()
        
        # Add to vector store
        if _global_db is None:
            logger.info("Creating new vector database from documents")
            _global_db = FAISS.from_documents(docs, embedding_model)
        else:
            logger.info("Adding documents to existing vector database")
            new_db = FAISS.from_documents(docs, embedding_model)
            _global_db.merge_from(new_db)
        
        # Save the updated index
        if not os.path.exists(index_path):
            os.makedirs(index_path)
        _global_db.save_local(index_path)
        
        logger.info(f"Successfully added {len(docs)} document chunks to vector store and saved to {index_path}")
        
    except Exception as e:
        logger.error(f"Error adding documents to vector store: {e}")
        raise
