from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

def create_vector(pdf_path: str, chunk_size=600, chunk_overlap=250):
    loader = PyPDFLoader(pdf_path)
    pages = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    documents = text_splitter.split_documents(pages)

    embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    db = Chroma.from_documents(documents, embedding_model)
    return db
