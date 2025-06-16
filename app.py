from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from rag import get_retriever

app = FastAPI()
retriever = get_retriever(k=5)

class Query(BaseModel):
    question: str

@app.post("/ask")
def ask_question(query: Query):
    try:
        docs = retriever.get_relevant_documents(query.question)
        results = [doc.page_content for doc in docs]
        return {"answers": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
