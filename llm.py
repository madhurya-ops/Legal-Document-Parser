from fastapi import FastAPI
from pydantic import BaseModel
import requests

app = FastAPI()

class UserInput(BaseModel):
    context: str
    prompt: str

HF_API_URL = "https://router.huggingface.co/featherless-ai/v1/chat/completions"

headers = {
    "Authorization": "",
    "Content-Type": "application/json"
}

def introduction(context: str, prompt: str) -> str:
    data = {
        "model": "mistralai/Mistral-7B-Instruct-v0.2",
        "messages": [
            {"role": "system", "content": context},
            {"role": "user", "content": prompt}
        ]
    }
    response = requests.post(HF_API_URL, headers=headers, json=data)
    print(response.text)  
    response.raise_for_status()  
    return response.json()["choices"][0]["message"]["content"]

@app.post("/gen")
def generate_introduction(user_input: UserInput):
    intro = introduction(user_input.context, user_input.prompt)
    return {"introduction": intro}