from langchain_community.document_loaders.pdf import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
import os
from tqdm import tqdm

# Settings
pdf_folder = "pdfs"  # your new folder with 14k PDFs
persist_directory = "chroma_db"
embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
text_splitter = RecursiveCharacterTextSplitter(chunk_size=600, chunk_overlap=250)

# Persistent vector DB connection
db = Chroma(persist_directory=persist_directory, embedding_function=embedding_model)

def get_existing_sources():
    """Fetch already embedded PDF filenames from Chroma metadata."""
    existing_sources = set()
    for doc in db.get()['metadatas']:
        if 'source' in doc:
            existing_sources.add(doc['source'])
    return existing_sources

def process_add_pdfs():
    pdf_files = [f for f in os.listdir(pdf_folder) if f.endswith(".pdf")]
    print(f"Found {len(pdf_files)} PDFs in dataset.")
    existing_sources = get_existing_sources()
    print(f"{len(existing_sources)} PDFs already in vector DB.")
    new_pdfs = [f for f in pdf_files if f not in existing_sources]
    print(f"🆕 {len(new_pdfs)} new PDFs to process.")
    if not new_pdfs:
        print(" No new PDFs to process.")
        return
    for filename in tqdm(new_pdfs, desc="Processing new PDFs"):
        file_path = os.path.join(pdf_folder, filename)
        try:
            loader = PyPDFLoader(file_path)
            pages = loader.load()
            documents = text_splitter.split_documents(pages)
            for doc in documents:
                doc.metadata["source"] = filename
            db.add_documents(documents)
        except Exception as e:
            print(f" Error processing {filename}: {e}")

    db.persist()
    print(" Vector database updated and saved.")

def get_retriever(k=5):
    return db.as_retriever(search_kwargs={"k": k})
