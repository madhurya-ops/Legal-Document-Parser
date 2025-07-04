import requests
import os
import json
import time
import logging
from dotenv import load_dotenv
from typing import Optional

# Load environment variables from .env (supports both backend/.env and root .env)
load_dotenv()

logger = logging.getLogger(__name__)

# Load Gemini API URL from environment, with fallback
GEMINI_API_URL = os.environ.get(
    'GEMINI_API_URL',
    "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"
)

gemini_api_key = os.environ.get('GEMINI_API_KEY')
if not gemini_api_key:
    raise RuntimeError("Gemini API key not set. Please set the GEMINI_API_KEY environment variable.")

# Cache for quick responses
response_cache = {}

def query(context: str, prompt: str) -> str:
    """Optimized query function for maximum speed and reliability."""
    
    # Check for immediate fallback cases
    prompt_lower = prompt.lower().strip()
    
    # Handle simple greetings immediately without API call
    if prompt_lower in ['hello', 'hi', 'hey', 'good morning', 'good afternoon', 'good evening']:
        return "Hello! I'm here to help with your legal document analysis. Please upload a document or ask a specific question."
    
    # Generate cache key
    cache_key = hash((prompt[:100], context[:500] if context else ""))
    if cache_key in response_cache:
        logger.info("Returning cached response")
        return response_cache[cache_key]
    
    # Load configuration for speed
    context_limit = 1500  # Reduced for faster processing
    prompt_limit = 400   # Reduced for faster processing
    
    # Truncate for speed
    if len(context) > context_limit:
        context = context[:context_limit] + "..."
    if len(prompt) > prompt_limit:
        prompt = prompt[:prompt_limit] + "..."
    
    # Simple, optimized prompt
    if context and context.strip():
        full_prompt = f"Based on this document: {context}\n\nQuestion: {prompt}\n\nProvide a brief, helpful answer:"
    else:
        # Quick fallback for no context
        if any(keyword in prompt_lower for keyword in ['document', 'contract', 'agreement', 'clause', 'analyze', 'extract', 'review']):
            return "Please upload a PDF, DOCX, or TXT document first, and then I'll analyze it for you."
        else:
            full_prompt = f"Question: {prompt}\n\nBrief answer:"
    
    # Fast API call with minimal configuration
    data = {
        "contents": [{"role": "user", "parts": [{"text": full_prompt}]}],
        "generationConfig": {
            "maxOutputTokens": 300,  # Reduced for speed
            "temperature": 0.3,      # Lower for consistency
            "topP": 0.8,
            "topK": 20               # Reduced for speed
        }
    }
    
    params = {"key": gemini_api_key}
    timeout = 10  # Aggressive timeout
    
    try:
        response = requests.post(GEMINI_API_URL, params=params, json=data, timeout=timeout)
        response.raise_for_status()
        resp_json = response.json()
        
        if "candidates" in resp_json and resp_json["candidates"]:
            parts = resp_json["candidates"][0].get("content", {}).get("parts", [])
            if parts and "text" in parts[0]:
                result = parts[0]["text"].strip()
                
                # Quick response limit
                if len(result) > 600:
                    result = result[:600] + "..."
                
                # Cache successful response
                response_cache[cache_key] = result
                
                # Limit cache size
                if len(response_cache) > 100:
                    # Remove oldest entries
                    keys_to_remove = list(response_cache.keys())[:20]
                    for key in keys_to_remove:
                        del response_cache[key]
                
                return result
                
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 429:
            return generate_quick_fallback(prompt, context)
        logger.error(f"API Error: {e.response.status_code}")
    except requests.exceptions.Timeout:
        logger.warning("Request timed out")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
    
    # Quick fallback
    return generate_quick_fallback(prompt, context)

def generate_quick_fallback(prompt: str, context: Optional[str] = None) -> str:
    """Generate ultra-fast fallback response"""
    prompt_lower = prompt.lower()
    
    # Pattern-based quick responses
    if any(word in prompt_lower for word in ['hello', 'hi', 'hey']):
        return "Hello! I'm here to help with legal document analysis."
    
    if any(word in prompt_lower for word in ['termination', 'terminate']):
        return "For termination clauses, look for sections about ending the agreement, notice periods, and termination conditions."
    
    if any(word in prompt_lower for word in ['payment', 'fee', 'compensation']):
        return "For payment terms, check sections about payment amounts, due dates, schedules, and late payment penalties."
    
    if any(word in prompt_lower for word in ['liability', 'indemnity']):
        return "For liability clauses, look for sections about damages, compensation, and responsibility allocation."
    
    if any(word in prompt_lower for word in ['jurisdiction', 'governing law']):
        return "For jurisdiction clauses, check sections about applicable law, court jurisdiction, and dispute resolution."
    
    if context and len(context) > 50:
        # Quick context-based response
        words = context.split()[:30]
        preview = ' '.join(words) + "..."
        return f"I can see your document contains: {preview}. Please ask a specific question about this content."
    
    return "I'm experiencing high demand right now. Please try rephrasing your question or try again in a moment."
    
    for attempt in range(max_retries):
        try:
            response = requests.post(GEMINI_API_URL, params=params, json=data, timeout=timeout)
            response.raise_for_status()
            resp_json = response.json()
            
            # Gemini returns candidates[0].content.parts[0].text
            if "candidates" in resp_json and resp_json["candidates"]:
                parts = resp_json["candidates"][0].get("content", {}).get("parts", [])
                if parts and "text" in parts[0]:
                    result = parts[0]["text"]
                    
                    # Truncate response if it exceeds the limit
                    response_limit = int(os.environ.get('RESPONSE_LIMIT', 800))
                    if len(result) > response_limit:
                        result = result[:response_limit] + "..."
                    
                    return result
            return "I apologize, but I couldn't generate a response at this time. This might be due to API limitations or the content of your query."
            
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 429:  # Rate limit error
                if fail_fast or attempt >= max_retries - 1:
                    # Provide helpful fallback response immediately
                    if context and context.strip():
                        return generate_fallback_response(prompt, context)
                    else:
                        return "I'm currently experiencing high demand. Please try again in a few minutes, or rephrase your question for better results."
                else:
                    print(f"Rate limit hit. Waiting {retry_delay} seconds before retry {attempt + 2}/{max_retries}...")
                    time.sleep(retry_delay)
                    continue
            else:
                return f"I encountered an API error. Please try rephrasing your question or try again later."
                
        except requests.exceptions.Timeout:
            if fail_fast or attempt >= max_retries - 1:
                return "Request timed out. Please try a shorter question or try again later."
            else:
                print(f"Request timed out. Retrying {attempt + 2}/{max_retries}...")
                time.sleep(2)  # Shorter delay for faster response
                continue
            
        except Exception as e:
            if fail_fast or attempt >= max_retries - 1:
                return "I encountered an unexpected error. Please try again with a different question."
            else:
                print(f"Unexpected error: {str(e)}. Retrying {attempt + 2}/{max_retries}...")
                time.sleep(2)
                continue
    
    # Fallback response if all retries failed
    if context and context.strip():
        return generate_fallback_response(prompt, context)
    else:
        return "I'm unable to process your request right now. Please try again later or contact support if the issue persists."

def generate_fallback_response(prompt: str, context: str) -> str:
    """Generate a simple fallback response when API is unavailable"""
    try:
        # Simple keyword-based responses for common queries
        prompt_lower = prompt.lower()
        
        if any(word in prompt_lower for word in ['hello', 'hi', 'hey']):
            return "Hello! I'm here to help with legal document analysis. Please upload a document and I'll assist you."
        
        if any(word in prompt_lower for word in ['termination', 'terminate']):
            return "I can see you're asking about termination clauses. While I can't process your request fully right now, please look for sections containing words like 'termination', 'end', 'expiry', or 'notice period' in your document."
        
        if any(word in prompt_lower for word in ['payment', 'fee', 'compensation']):
            return "You're asking about payment terms. Look for sections mentioning payment schedules, amounts, due dates, and late payment penalties in your document."
        
        if any(word in prompt_lower for word in ['liability', 'indemnity']):
            return "For liability and indemnity clauses, check sections that mention damages, compensation, responsibility, or hold harmless provisions."
        
        if context:
            # Extract first few sentences from context as a basic response
            sentences = context.split('.')[:3]
            return f"Based on your document, here's what I can see: {'. '.join(sentences)}. Please try your question again in a few minutes for a more detailed analysis."
        
        return "I'm having trouble processing your request right now. Please try again in a few minutes or rephrase your question."
        
    except Exception:
        return "I'm currently unable to process requests. Please try again later."
