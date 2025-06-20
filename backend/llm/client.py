import requests
import os

HF_API_URL = "https://router.huggingface.co/novita/v3/openai/chat/completions"

# Correct API key usage
api_key = os.environ.get('HF_API_KEY')
if not api_key or api_key == '':
    raise RuntimeError("HuggingFace API key not set. Please set the HF_API_KEY environment variable.")

headers = {
    "Authorization": f"Bearer {api_key}",
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
    print("HuggingFace API response:", response.text)
    response.raise_for_status()
    resp_json = response.json()
    # Robustly handle the response structure
    if "choices" in resp_json and resp_json["choices"] and "message" in resp_json["choices"][0] and "content" in resp_json["choices"][0]["message"]:
        return resp_json["choices"][0]["message"]["content"]
    else:
        print("Unexpected HuggingFace API response structure:", resp_json)
        return "Sorry, the language model did not return a valid response. Please try again later."
