from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from rag import create_vector
from llm import query

app = FastAPI()
db = create_vector("any.pdf")

class Query(BaseModel):
    question: str
    
@app.post("/ask")
def ask_question(query: Query):
    try:
        retriever = db.as_retriever(search_kwargs={"k": 5})
        retrieved_docs = retriever.get_relevant_documents(query.question)
        context = "\n\n".join([doc.page_content for doc in retrieved_docs])
        answer = query(context=context, prompt=query.question)
        return {"answer": answer}
    except Exception as e:
        print(f"Error processing query: {e}")
        raise HTTPException(status_code=500, detail="Error generating answer")

@app.get("/check")
def health_check():
    return {"status": "ok"}
