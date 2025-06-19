from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.core.vector_store import get_retriever

router = APIRouter()

# Initialize retriever once at module level
retriever = get_retriever(k=5)

class Query(BaseModel):
    question: str

@router.post("/ask")
def ask_question(query: Query):
    try:
        docs = retriever.get_relevant_documents(query.question)
        results = [doc.page_content for doc in docs]
        return {"answers": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
