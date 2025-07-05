import requests
import os
import json
from dotenv import load_dotenv

# Load environment variables from .env (supports both backend/.env and root .env)
load_dotenv()

GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"

gemini_api_key = os.environ.get('GEMINI_API_KEY')
if not gemini_api_key:
    raise RuntimeError("Gemini API key not set. Please set the GEMINI_API_KEY environment variable.")

def query(context: str, prompt: str) -> str:
    # Load system prompt from environment, fallback to default
    system_instruction = os.environ.get(
        "SYSTEM_PROMPT",
        "You are a helpful, friendly, and professional legal assistant. "
        "You may respond to greetings, small talk, and polite conversation in a natural, human-like way but only very short answers only. Greeting and small talks must not be more than 1 line. Do not give any information unless asked by the user explicitely, answer or talk only as much as required. "
        "For legal or document-related questions, answer only if the information is present in the provided context/database. "
        "If you do not know the answer or it is not present in the context, say 'I don't know' or politely indicate you cannot answer. "
        "Do not make up information or hallucinate. Stay within the scope of the provided legal documents and data. "
        "If a user asks something completely out of scope (not a greeting, small talk, or legal/document question), politely decline to answer."

    )
    # Gemini expects a single prompt string, but we can concatenate context and prompt
    if len(context) > 2500:
        context = context[:2500] + "..."
    if len(prompt) > 800:
        prompt = prompt[:800] + "..."
    
    # Handle special case where no documents are uploaded
    if context.startswith("NO_DOCUMENTS_UPLOADED:"):
        return "I don't see any documents uploaded to analyze. Please upload a PDF, DOCX, or TXT file first, and then I'll be happy to help you analyze its contents, extract key information, or answer questions about it."
    
    # Combine system instruction, context, and prompt
    full_prompt = system_instruction + "Context:\n" + context + "\n\nQuestion: " + prompt
    
    # Gemini expects a 'contents' list with 'role' and 'parts'
    data = {
        "contents": [
            {"role": "user", "parts": [{"text": full_prompt}]}
        ],
        "generationConfig": {
            "maxOutputTokens": 500,
            "temperature": 0.7
        }
    }
    params = {"key": gemini_api_key}
    try:
        response = requests.post(GEMINI_API_URL, params=params, json=data, timeout=30)
        response.raise_for_status()
        resp_json = response.json()
        # Gemini returns candidates[0].content.parts[0].text
        if "candidates" in resp_json and resp_json["candidates"]:
            parts = resp_json["candidates"][0].get("content", {}).get("parts", [])
            if parts and "text" in parts[0]:
                result = parts[0]["text"]
                if len(result) > 800:
                    result = result[:800] + "..."
                return result
        return "Sorry, the language model did not return a valid response. Please try again later."
    except requests.exceptions.Timeout:
        return "Request timed out. Please try again."
    except Exception as e:
        return f"Error: {str(e)[:100]}"
# update Sun Jul  6 02:54:59 IST 2025
