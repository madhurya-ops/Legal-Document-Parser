import requests
import os
from app.core.config import SYSTEM_PROMPT
HF_API_URL = "https://router.huggingface.co/featherless-ai/v1/chat/completions"

headers = {
    "Authorization": os.getenv("HF_API_KEY"),
    "Content-Type": "application/json"
}
def query_llm(prompt: str, context: str = SYSTEM_PROMPT) -> str:
    data = {
        "model": "mistralai/Mistral-7B-Instruct-v0.2",
        "messages": [
            {"role": "system", "content": context},
            {"role": "user", "content": prompt}
        ]
    }
    response = requests.post(HF_API_URL, headers=headers, json=data)
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]
