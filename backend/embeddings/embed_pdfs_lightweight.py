import os
import sys
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import pickle
import gc
import uuid
import logging

# Fix import path for pdf_config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
try:
    from pdf_config import get_config
    # Get configuration based on deployment tier
    config = get_config('free')  # Change to 'paid' for more generous limits
except ImportError:
    logging.warning("pdf_config not found, using default conservative settings")
    # Default conservative settings for Render free tier
    config = {
        'MAX_PDF_SIZE_MB': 1,
        'MAX_PAGES': 3,
        'MAX_CHUNKS': 20,
        'MAX_CHUNKS_PER_PAGE': 3,
        'CHUNK_SIZE': 100,
        'BATCH_SIZE': 3
    }

# Setup basic logging for the script
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Settings - Ultra lightweight with configurable limits
pdf_folder = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "pdfs")
index_path = "index"
MAX_PDF_SIZE_MB = config['MAX_PDF_SIZE_MB']
MAX_PAGES = config['MAX_PAGES']
MAX_CHUNKS = config['MAX_CHUNKS']
MAX_CHUNKS_PER_PAGE = config['MAX_CHUNKS_PER_PAGE']
CHUNK_SIZE = config['CHUNK_SIZE']
BATCH_SIZE = config['BATCH_SIZE']

def get_file_size_mb(filepath):
    """Get file size in MB"""
    try:
        return os.path.getsize(filepath) / (1024 * 1024)
    except:
        return 0

def process_and_store_pdfs_lightweight():
    """Lightweight PDF processing with strict limits"""
    # Check if uploads directory exists
    if not os.path.exists(pdf_folder):
        logging.info(f"Uploads directory '{pdf_folder}' does not exist. Creating it...")
        os.makedirs(pdf_folder)
        logging.info("No documents to process.")
        return
    
    pdf_files = [f for f in os.listdir(pdf_folder) if f.endswith(('.pdf', '.docx', '.txt'))]
    logging.info(f"Found {len(pdf_files)} documents in uploads folder.")
    logging.info(f"Using limits: {MAX_PDF_SIZE_MB}MB max, {MAX_PAGES} pages, {MAX_CHUNKS} chunks")

    if not pdf_files:
        logging.info("No documents to process.")
        return

    documents = []
    total_chunks = 0
    
    # Process one document at a time with strict limits
    for filename in tqdm(pdf_files, desc="Processing documents"):
        try:
            filepath = os.path.join(pdf_folder, filename)
            file_size = get_file_size_mb(filepath)
            
            # Skip large files
            if file_size > MAX_PDF_SIZE_MB:
                logging.warning(f"Skipping {filename} - too large ({file_size:.1f}MB > {MAX_PDF_SIZE_MB}MB)")
                continue
                
            logging.info(f"Processing {filename} ({file_size:.1f}MB)...")
            
            # Load document with page limit
            try:
                if filename.endswith('.pdf'):
                    loader = PyPDFLoader(filepath)
                    pages = loader.load()
                elif filename.endswith('.txt'):
                    # Handle text files
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                    from langchain.schema import Document
                    pages = [Document(page_content=content, metadata={"source": filename})]
                else:
                    # Skip unsupported file types for now
                    logging.warning(f"Skipping {filename} - unsupported file type")
                    continue
            except Exception as e:
                logging.error(f"Error loading {filename}: {e}")
                continue
            
            # Limit pages
            if len(pages) > MAX_PAGES:
                logging.info(f"Limiting {filename} to first {MAX_PAGES} pages (total: {len(pages)})")
                pages = pages[:MAX_PAGES]
            
            # Process pages with strict limits
            for i, page in enumerate(pages):
                if total_chunks >= MAX_CHUNKS:
                    logging.warning(f"Reached maximum chunks limit ({MAX_CHUNKS})")
                    break
                    
                try:
                    # Use very small chunks
                    text_splitter = RecursiveCharacterTextSplitter(
                        chunk_size=CHUNK_SIZE,
                        chunk_overlap=20,  # Restored to original for better context
                        length_function=len,
                        separators=["\n\n", "\n", ". ", " ", ""]
                    )
                    
                    split_docs = text_splitter.split_documents([page])
                    
                    # Limit chunks per page
                    if len(split_docs) > MAX_CHUNKS_PER_PAGE:
                        split_docs = split_docs[:MAX_CHUNKS_PER_PAGE]
                    
                    for doc in split_docs:
                        doc.metadata["source"] = filename
                        doc.metadata["page"] = i + 1
                        documents.append(doc)
                        total_chunks += 1
                        
                        if total_chunks >= MAX_CHUNKS:
                            break
                    
                    # Clear memory after each page
                    del split_docs
                    gc.collect()
                    
                except Exception as e:
                    logging.error(f"Error processing page {i+1} of {filename}: {e}")
                    continue
                    
                if total_chunks >= MAX_CHUNKS:
                    break
            
            # Clear page memory after each file
            del pages
            gc.collect()
                    
        except Exception as e:
            logging.error(f"Error processing {filename}: {e}")
            continue

    if documents:
        logging.info(f"Successfully processed {len(documents)} chunks")
        
        # Create minimal index
        try:
            # Use a very simple embedding approach
            from sentence_transformers import SentenceTransformer
            
            # Load the lightest possible model
            try:
                model = SentenceTransformer('paraphrase-MiniLM-L3-v2')
            except:
                # Fallback to even lighter model
                model = SentenceTransformer('all-MiniLM-L6-v2')
            
            # Create embeddings in very small batches
            texts_for_embedding = [doc.page_content for doc in documents]
            
            all_embeddings = []
            for i in range(0, len(texts_for_embedding), BATCH_SIZE):
                batch_texts = texts_for_embedding[i:i + BATCH_SIZE]
                
                # Get embeddings
                embeddings = model.encode(batch_texts, convert_to_tensor=False)
                all_embeddings.extend(embeddings.tolist())
                
                # Clear memory
                del batch_texts, embeddings
                gc.collect()
            
            # Clear the large list of texts
            del texts_for_embedding
            gc.collect()

            # Create simple FAISS index
            import numpy as np
            import faiss
            
            embeddings_array = np.array(all_embeddings).astype('float32')
            
            # Create index
            dimension = embeddings_array.shape[1]
            index = faiss.IndexFlatIP(dimension)
            index.add(embeddings_array)
            
            # Save index and documents
            if not os.path.exists(index_path):
                os.makedirs(index_path)
                
            faiss.write_index(index, f"{index_path}/faiss.index")
            
            with open(f"{index_path}/documents.pkl", "wb") as f:
                pickle.dump(documents, f)
                
            logging.info(f"Lightweight FAISS index saved to {index_path}")
            logging.info(f"Index contains {len(documents)} chunks with {dimension}-dimensional embeddings")
            
            # Clear large objects
            del embeddings_array, all_embeddings, index
            gc.collect()
            
        except Exception as e:
            logging.error(f"Error creating index: {e}")
            # Save empty index as fallback
            try:
                if not os.path.exists(index_path):
                    os.makedirs(index_path)
                import faiss
                index = faiss.IndexFlatIP(384)
                faiss.write_index(index, f"{index_path}/faiss.index")
                with open(f"{index_path}/documents.pkl", "wb") as f:
                    pickle.dump([], f)
                logging.info("Saved empty index as fallback")
            except Exception as e2:
                logging.error(f"Failed to save fallback index: {e2}")
    else:
        logging.info("No documents processed.")

if __name__ == "__main__":
    from tqdm import tqdm
    process_and_store_pdfs_lightweight() # update Sun Jul  6 02:54:59 IST 2025
