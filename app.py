from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from rag import create_vector
from llm import query as llm_query  # ✅ Rename to avoid conflict

app = FastAPI()

# Enable CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create the vector DB once on startup
db = create_vector("any.pdf")

# Request schema
class QueryRequest(BaseModel):
    question: str

# Ask endpoint
@app.post("/ask")
def ask_question(payload: QueryRequest):
    try:
        retriever = db.as_retriever(search_kwargs={"k": 5})
        retrieved_docs = retriever.get_relevant_documents(payload.question)
        context = "\n\n".join([doc.page_content for doc in retrieved_docs])
        answer = llm_query(context=context, prompt=payload.question)  # ✅ Correct function call
        return {"answer": answer}
    except Exception as e:
        print(f"Error processing query: {e}")
        raise HTTPException(status_code=500, detail="Error generating answer")

# Health check
@app.get("/check")
def health_check():
    return {"status": "ok"}