from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from app.core.vector_store import get_retriever
from llm.client import query

router = APIRouter()

# Initialize retriever once at module level
retriever = get_retriever(k=5)

class Query(BaseModel):
    question: str
    file_content: Optional[str] = None

@router.post("/ask")
def ask_question(query_data: Query):
    try:
        docs = retriever.get_relevant_documents(query_data.question)
        context = "\n\n".join([doc.page_content for doc in docs])
        # If file_content is provided, add it to the context
        if query_data.file_content:
            context = f"{query_data.file_content}\n\n{context}"
        answer = query(context, query_data.question)
        if not answer or not str(answer).strip():
            answer = "Sorry, the language model did not return a valid response. Please try again later."
        return {"answer": answer}
    except Exception as e:
        print("Error in /ask endpoint:", e)
        raise HTTPException(status_code=500, detail=str(e))
