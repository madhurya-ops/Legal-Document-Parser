import requests
import os

HF_API_URL = "https://router.huggingface.co/novita/v3/openai/chat/completions"

api_key = os.environ.get('HF_API_KEY')
if not api_key:
    raise RuntimeError("HuggingFace API key not set. Please set the HF_API_KEY environment variable.")

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

def query(context: str, prompt: str) -> str:
    # Limit context and prompt size to reduce memory usage while preserving functionality
    if len(context) > 2500:  # Increased from 1500 to preserve more context
        context = context[:2500] + "..."
    
    if len(prompt) > 800:  # Increased from 500 to allow longer questions
        prompt = prompt[:800] + "..."
    
    data = {
        "model": "mistralai/Mistral-7B-Instruct-v0.2",
        "messages": [
            {"role": "system", "content": context},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 500,  # Increased from 300 to allow longer responses
        "temperature": 0.7
    }
    
    try:
        response = requests.post(HF_API_URL, headers=headers, json=data, timeout=30)
        response.raise_for_status()
        
        resp_json = response.json()
        if "choices" in resp_json and resp_json["choices"] and "message" in resp_json["choices"][0]:
            result = resp_json["choices"][0]["message"]["content"]
            # Limit response size but allow longer responses
            if len(result) > 800:  # Increased from 500
                result = result[:800] + "..."
            return result
        else:
            return "Sorry, the language model did not return a valid response. Please try again later."
    except requests.exceptions.Timeout:
        return "Request timed out. Please try again."
    except Exception as e:
        return f"Error: {str(e)[:100]}"