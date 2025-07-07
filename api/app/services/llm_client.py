import requests
import os
import json
import logging
import random
from datetime import datetime
from dotenv import load_dotenv
from typing import Optional, Dict, List, Any

from ..core.config import get_settings

logger = logging.getLogger(__name__)

def get_greeting() -> str:
    """Generate appropriate greeting based on time of day with Indian touch"""
    hour = datetime.now().hour
    if 5 <= hour < 12:
        return random.choice(["Namaste! ", "Shubh prabhat! ", "Good morning! "])
    elif 12 <= hour < 17:
        return random.choice(["Namaste! ", "Shubh dina! ", "Good afternoon! "])
    else:
        return random.choice(["Namaste! ", "Shubh sandhya! ", "Good evening! "])

# Lazy loading for settings to avoid module-level instantiation
_gemini_api_key = None
_gemini_api_url = None

def get_gemini_api_key():
    global _gemini_api_key
    if _gemini_api_key is None:
        settings = get_settings()
        _gemini_api_key = settings.GEMINI_API_KEY
        if not _gemini_api_key:
            logger.warning("Gemini API key not set. LLM functionality may be limited.")
    return _gemini_api_key

def get_gemini_api_url():
    global _gemini_api_url
    if _gemini_api_url is None:
        settings = get_settings()
        _gemini_api_url = getattr(settings, 'GEMINI_API_URL', None) or (
            "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"
        )
    return _gemini_api_url

# Cache for quick responses
response_cache = {}

def clean_response_formatting(text: str) -> str:
    """Clean up response formatting - remove asterisks and improve readability."""
    if not text:
        return text
    
    # Remove asterisk-based formatting (bold/italic markdown)
    text = text.replace('**', '')
    text = text.replace('*', '')
    
    # Clean up extra whitespace and line breaks
    lines = text.split('\n')
    cleaned_lines = []
    
    for line in lines:
        line = line.strip()
        if line:  # Only keep non-empty lines
            cleaned_lines.append(line)
    
    # Join with proper spacing
    result = '\n\n'.join(cleaned_lines)
    
    # Remove any remaining multiple spaces
    import re
    result = re.sub(r' +', ' ', result)
    
    return result.strip()

async def query_gemini(context: str, prompt: str) -> str:
    """Enhanced query function for legal document analysis and legal questions."""
    # Generate cache key
    cache_key = hash((prompt[:100], context[:500] if context else ""))
    if cache_key in response_cache:
        logger.info("Returning cached response")
        return response_cache[cache_key]
    
    # Handle empty or greeting prompts with comprehensive legal introduction
    prompt_lower = prompt.lower().strip()
    if not prompt_lower or any(word in prompt_lower for word in ['hello', 'hi', 'hey', 'namaste', 'namaskar']):
        greeting = get_greeting()
        full_prompt = f"""{greeting}You are an expert legal assistant specializing in Indian law. Provide a comprehensive introduction to your capabilities.

In your response, include:
1. A warm greeting
2. Your role as a legal AI assistant
3. Key areas of expertise (Indian law, legal document analysis, etc.)
4. Types of legal questions you can help with
5. How users can interact with you
6. Any disclaimers about legal advice

Format your response in clear, well-structured paragraphs."""
    else:
        # For all other queries, use the LLM to generate comprehensive responses
        greeting = get_greeting()
        
        # Check if this is a document analysis request
        if context and context.strip() and not context.startswith("Unable to extract"):
            # Document analysis prompt
            full_prompt = f"""{greeting}You are an expert legal analyst. Provide a comprehensive analysis of the following legal document.

DOCUMENT CONTENT:
{context[:10000]}  # Limit context to prevent token limits

USER'S QUESTION:
{prompt if prompt else 'Please analyze this document'}

Your analysis should include:
1. Document type and purpose
2. Key parties involved
3. Main obligations and rights
4. Important clauses and their implications
5. Potential legal risks or concerns
6. Recommendations for next steps
7. Relevant laws and regulations
8. Any additional insights or observations

Provide a detailed, well-structured response with clear headings for each section."""
        else:
            # General legal question prompt
            full_prompt = f"""{greeting}You are an expert legal advisor specializing in Indian law. Provide a comprehensive answer to the following legal question.

QUESTION:
{prompt}

In your response, please include:
1. A clear, direct answer to the question
2. Relevant laws, acts, and sections
3. Important case laws and precedents
4. Practical implications and considerations
5. Step-by-step legal procedures if applicable
6. Potential outcomes and their likelihood
7. Recommendations for next steps
8. Any warnings or important limitations

Structure your response with clear headings and use plain language to explain complex legal concepts."""
    
    # Enhanced API call configuration for optimal legal responses
    data = {
        "contents": [{
            "role": "user",
            "parts": [{
                "text": full_prompt
            }]
        }],
        "generationConfig": {
            "maxOutputTokens": 2000,
            "temperature": 0.3,
            "topP": 0.8,
            "topK": 30,
            "stopSequences": ["###", "---", "==="]
        },
        "safetySettings": [
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_NONE"
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_NONE"
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_NONE"
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_NONE"
            }
        ]
    }
    
    params = {"key": get_gemini_api_key()}
    timeout = 30
    max_retries = 2
    retry_delay = 2
    
    for attempt in range(max_retries + 1):
        try:
            response = requests.post(get_gemini_api_url(), params=params, json=data, timeout=timeout)
            response.raise_for_status()
            resp_json = response.json()
            
            if "candidates" in resp_json and resp_json["candidates"]:
                parts = resp_json["candidates"][0].get("content", {}).get("parts", [])
                if parts and "text" in parts[0]:
                    result = parts[0]["text"].strip()
                    
                    # Clean up the response
                    result = clean_response_formatting(result)
                    
                    # Ensure response is not too verbose
                    if len(result) > 3000:
                        result = result[:3000] + "...\n\n[Response truncated due to length]"
                    
                    # Cache successful response
                    response_cache[cache_key] = result
                    
                    # Limit cache size
                    if len(response_cache) > 100:
                        keys_to_remove = list(response_cache.keys())[:20]
                        for key in keys_to_remove:
                            del response_cache[key]
                    
                    return result
            
            logger.error(f"Unexpected response format: {resp_json}")
            break
                
        except requests.exceptions.HTTPError as e:
            status_code = getattr(e.response, 'status_code', None)
            if status_code == 429:  # Rate limit
                if attempt < max_retries:
                    import time
                    time.sleep(retry_delay * (attempt + 1))
                    continue
                logger.warning("Rate limit reached, using fallback response")
            else:
                logger.error(f"API Error {status_code}: {str(e)}")
            break
                
        except requests.exceptions.Timeout:
            if attempt < max_retries:
                import time
                time.sleep(retry_delay * (attempt + 1))
                continue
            logger.warning("Request timed out after multiple retries")
            break
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed: {str(e)}")
            break
            
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}", exc_info=True)
            break
    
    # If we get here, all retries failed or an error occurred
    greeting = get_greeting()
    return f"""{greeting}I apologize, but I'm having trouble processing your request at the moment. 

This might be due to high server load or temporary connectivity issues. 

Please try one of the following:
1. Rephrase your question
2. Try again in a few moments
3. Break down complex questions into simpler ones
4. Ensure your document is in a supported format

If the issue persists, please contact support with details of your query."""

def generate_intelligent_fallback(prompt: str, context: Optional[str] = None) -> str:
    """Generate helpful fallback responses for legal questions when the main API fails."""
    if not prompt.strip():
        return get_greeting() + "I'm here to help with your legal questions. Please ask me anything about Indian law."
    
    prompt_lower = prompt.lower()
    greeting = get_greeting()
    
    # Common legal categories
    legal_categories = {
        'criminal': ['murder', 'assault', 'theft', 'fraud', 'cheating', 'rape', 'kidnapping', 'bail', 'arrest', 'fir'],
        'civil': ['contract', 'agreement', 'property', 'rent', 'lease', 'tort', 'negligence', 'damages'],
        'family': ['divorce', 'maintenance', 'custody', 'adoption', 'dowry', 'domestic violence', 'maintenance'],
        'corporate': ['company', 'incorporation', 'board', 'director', 'shares', 'meeting', 'compliance', 'mca'],
        'property': ['sale deed', 'title', 'possession', 'partition', 'gift', 'will', 'succession', 'inheritance'],
        'intellectual': ['trademark', 'copyright', 'patent', 'design', 'ipr', 'intellectual property'],
        'constitutional': ['fundamental rights', 'article 14', 'article 19', 'article 21', 'writ', 'constitution'],
        'tax': ['income tax', 'gst', 'vat', 'tds', 'return', 'assessment', 'appeal', 'notice']
    }
    
    # Identify the most relevant legal category
    matched_category = None
    for category, keywords in legal_categories.items():
        if any(keyword in prompt_lower for keyword in keywords):
            matched_category = category
            break
    
    # Generate category-specific guidance
    if matched_category:
        return f"""{greeting}I can help with {matched_category} law matters. Here's some general information:

{get_legal_guidance(matched_category, prompt_lower)}

For specific legal advice, please consult with a qualified attorney who can review the details of your situation."""
    
    # General legal guidance for unmatched categories
    return f"""{greeting}I'm here to help with your legal query about "{prompt}".

While I can provide general legal information, please note that I cannot provide specific legal advice. For personalized assistance, consider:

1. Consulting with a qualified attorney
2. Visiting the nearest legal aid clinic
3. Contacting the State/District Legal Services Authority
4. Checking official government websites for relevant laws and procedures

Would you like me to help you find relevant legal resources or explain general legal concepts related to your query?"""

def get_legal_guidance(category: str, query: str) -> str:
    """Provide basic legal guidance for different categories."""
    guidance = {
        'criminal': """Criminal Law in India:
- Governed by the Indian Penal Code (IPC), 1860 and Criminal Procedure Code (CrPC), 1973
- Deals with offenses against the state/society
- Key stages: FIR, investigation, chargesheet, trial, judgment, appeal
- Rights of the accused include right to bail, legal representation, and fair trial
- Punishments range from fines to imprisonment or death penalty for serious offenses""",
        
        'civil': """Civil Law in India:
- Deals with disputes between individuals/organizations
- Includes contracts, property disputes, torts, and more
- Governed by various acts like Indian Contract Act, Transfer of Property Act, etc.
- Remedies include compensation, injunction, specific performance
- Cases are decided on the balance of probabilities""",
        
        'family': """Family Law in India:
- Governed by personal laws based on religion (Hindu, Muslim, Christian, etc.)
- Covers marriage, divorce, maintenance, custody, adoption
- Special Marriage Act provides for inter-religion marriages
- Domestic Violence Act provides protection to women
- Child custody decisions are based on the child's best interests""",
        
        'property': """Property Law in India:
- Governed by Transfer of Property Act, Registration Act, various state laws
- Types: Movable and immovable property
- Important documents: Title deed, sale deed, encumbrance certificate
- Registration is mandatory for certain transactions
- Succession laws determine inheritance rights"""
    }
    
    return guidance.get(category, "I can provide general information about this legal topic. Please ask specific questions for more detailed guidance.")

# Sync wrapper for backward compatibility
def query(context: str, prompt: str) -> str:
    """Synchronous wrapper for the async query function."""
    import asyncio
    try:
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(query_gemini(context, prompt))
    except RuntimeError:
        # No event loop running, create a new one
        return asyncio.run(query_gemini(context, prompt))
