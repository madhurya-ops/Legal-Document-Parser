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
<<<<<<< HEAD
        results = [doc.page_content for doc in docs]
        return {"answers": results}
=======
        context = "\n\n".join([doc.page_content for doc in docs])
        # If file_content is provided, add it to the context
        if query.file_content:
            context = f"{query.file_content}\n\n{context}"
        answer = query_llm(query.question, context)
        if not answer or not str(answer).strip():
            answer = "Sorry, the language model did not return a valid response. Please try again later."
        return {"answer": answer}
>>>>>>> 5721d64 (Added functional dynamic Frontend integrated with Backend.)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
