from fastapi import FastAPI
from pydantic import BaseModel
import requests
app = FastAPI()
class UserInput(BaseModel):
    context: str
    prompt: str
HF_API_URL = "https://router.huggingface.co/hf-inference/models/mistralai/Mistral-7B-Instruct-v0.3/v1/chat/completions"
headers = {
    "Authorization": "",
    "Content-Type": "application/json"
}
def introduction(context: str, prompt: str) -> str:
    data = {
        "messages": [
            {"role": "system", "content": f"{context}"},
            {"role": "user", "content": f"{prompt}"}
        ]
    }
    response = requests.post(HF_API_URL, headers=headers, json=data)
    return response.json().get("choices")[0]["message"]["content"]

@app.post("/gen")
def generate_introduction(user_input: UserInput):
    intro = introduction(user_input.context, user_input.prompt)
    return {"introduction": intro}

