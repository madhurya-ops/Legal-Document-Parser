import requests
import os

HF_API_URL = "https://router.huggingface.co/featherless-ai/v1/chat/completions"

headers = {
    "Authorization": "Bearer",
    "Content-Type": "application/json"
}

def query(context: str, prompt: str) -> str:
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
