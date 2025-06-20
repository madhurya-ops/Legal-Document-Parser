import os
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from tqdm import tqdm
import pickle

# Settings
pdf_folder = "pdfs"
index_path = "index"
embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
text_splitter = RecursiveCharacterTextSplitter(chunk_size=600, chunk_overlap=250)

def process_and_store_pdfs():
    pdf_files = [f for f in os.listdir(pdf_folder) if f.endswith(".pdf")]
    print(f"Found {len(pdf_files)} PDFs.")

    if not pdf_files:
        print("No PDFs to process.")
        return

    documents = []
    for filename in tqdm(pdf_files, desc="Processing PDFs"):
        try:
            loader = PyPDFLoader(os.path.join(pdf_folder, filename))
            pages = loader.load()
            split_docs = text_splitter.split_documents(pages)
            for doc in split_docs:
                doc.metadata["source"] = filename
            documents.extend(split_docs)
        except Exception as e:
            print(f"Error processing {filename}: {e}")

    if documents:
        print(f"Embedding {len(documents)} documents...")
        db = FAISS.from_documents(documents, embedding_model)
        db.save_local(index_path)
        print(f"FAISS vector store saved to {index_path}.")
    else:
        print("No documents processed.")

if __name__ == "__main__":
    process_and_store_pdfs()
