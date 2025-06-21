import os
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from tqdm import tqdm
import pickle
import gc

# Settings - More memory efficient
pdf_folder = "pdfs"
index_path = "index"

# Use a lighter embedding model for memory efficiency
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

# Smaller chunks for memory efficiency
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=300,  # Reduced from 600
    chunk_overlap=50,  # Reduced from 250
    length_function=len,
    separators=["\n\n", "\n", " ", ""]
)

def process_and_store_pdfs():
    pdf_files = [f for f in os.listdir(pdf_folder) if f.endswith(".pdf")]
    print(f"Found {len(pdf_files)} PDFs.")

    if not pdf_files:
        print("No PDFs to process.")
        return

    documents = []
    
    # Process one PDF at a time to save memory
    for filename in tqdm(pdf_files, desc="Processing PDFs"):
        try:
            print(f"Processing {filename}...")
            loader = PyPDFLoader(os.path.join(pdf_folder, filename))
            pages = loader.load()
            
            # Process pages in smaller batches
            for i, page in enumerate(pages):
                try:
                    split_docs = text_splitter.split_documents([page])
                    for doc in split_docs:
                        doc.metadata["source"] = filename
                        doc.metadata["page"] = i + 1
                    documents.extend(split_docs)
                    
                    # Clear memory after each page
                    del split_docs
                    gc.collect()
                    
                except Exception as e:
                    print(f"Error processing page {i+1} of {filename}: {e}")
                    continue
                    
        except Exception as e:
            print(f"Error processing {filename}: {e}")
            continue

    if documents:
        print(f"Embedding {len(documents)} documents...")
        try:
            # Process documents in smaller batches
            batch_size = 50  # Process 50 documents at a time
            all_embeddings = []
            
            for i in range(0, len(documents), batch_size):
                batch = documents[i:i + batch_size]
                print(f"Processing batch {i//batch_size + 1}/{(len(documents) + batch_size - 1)//batch_size}")
                
                # Create embeddings for this batch
                texts = [doc.page_content for doc in batch]
                embeddings = embedding_model.embed_documents(texts)
                all_embeddings.extend(embeddings)
                
                # Clear memory
                del batch, texts, embeddings
                gc.collect()
            
            # Create FAISS index from embeddings
            import numpy as np
            embeddings_array = np.array(all_embeddings)
            
            # Create FAISS index
            dimension = embeddings_array.shape[1]
            import faiss
            index = faiss.IndexFlatIP(dimension)  # Inner product for normalized embeddings
            index.add(embeddings_array.astype('float32'))
            
            # Save the index and documents
            faiss.write_index(index, f"{index_path}/faiss.index")
            
            # Save documents separately
            with open(f"{index_path}/documents.pkl", "wb") as f:
                pickle.dump(documents, f)
                
            print(f"FAISS vector store saved to {index_path}.")
            
        except Exception as e:
            print(f"Error saving vector store: {e}")
            # Try to save a minimal index
            try:
                if not os.path.exists(index_path):
                    os.makedirs(index_path)
                # Save empty index as fallback
                import faiss
                index = faiss.IndexFlatIP(384)  # Default dimension
                faiss.write_index(index, f"{index_path}/faiss.index")
                with open(f"{index_path}/documents.pkl", "wb") as f:
                    pickle.dump([], f)
                print("Saved empty index as fallback.")
            except Exception as e2:
                print(f"Failed to save fallback index: {e2}")
    else:
        print("No documents processed.")

if __name__ == "__main__":
    config = get_config('free')  # Conservative limits
    process_and_store_pdfs()
