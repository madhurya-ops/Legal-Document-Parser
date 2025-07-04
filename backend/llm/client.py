import requests
import os
import json
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

def clean_response_formatting(text: str) -> str:
    """Clean up response formatting - remove asterisks and improve readability."""
    if not text:
        return text
    
    # Remove asterisk-based formatting (bold/italic markdown)
    # Convert **bold** to just bold text without asterisks
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

def query(context: str, prompt: str) -> str:
    """Enhanced query function for proper legal responses."""
    
    # Check for immediate fallback cases
    prompt_lower = prompt.lower().strip()
    
    # Handle simple greetings immediately without API call
    if prompt_lower in ['hello', 'hi', 'hey', 'good morning', 'good afternoon', 'good evening']:
        return "Hello! I'm here to help with your legal questions and document analysis. Feel free to ask about Indian law, contracts, or upload a document for analysis."
    
    # Generate cache key
    cache_key = hash((prompt[:100], context[:500] if context else ""))
    if cache_key in response_cache:
        logger.info("Returning cached response")
        return response_cache[cache_key]
    
    # Load configuration for better responses
    context_limit = 2000  # Increased for better context
    prompt_limit = 500    # Increased for better prompts
    
    # Truncate for optimal balance
    if len(context) > context_limit:
        context = context[:context_limit] + "..."
    if len(prompt) > prompt_limit:
        prompt = prompt[:prompt_limit] + "..."
    
    # Enhanced prompting system
    if context and context.strip() and not context.startswith("Unable to extract"):
        # Document analysis mode
        full_prompt = f"""You are a legal assistant specializing in Indian law. 
        
Document Content: {context}

User Question: {prompt}

Please provide a detailed, helpful analysis based on the document content. If the question is about general legal concepts, explain them in the context of Indian law."""
    else:
        # General legal question mode - don't require document upload
        full_prompt = f"""You are a legal assistant specializing in Indian law. Answer the following question with detailed, accurate information about Indian legal concepts, laws, and practices.

Question: {prompt}

Provide a comprehensive answer covering:
1. Definition and explanation
2. Relevant Indian laws and regulations
3. Practical implications
4. Key points to remember

Answer:"""
    
    # Enhanced API call configuration for better responses
    data = {
        "contents": [{"role": "user", "parts": [{"text": full_prompt}]}],
        "generationConfig": {
            "maxOutputTokens": 800,   # Increased for detailed responses
            "temperature": 0.4,       # Balanced for accuracy and detail
            "topP": 0.9,
            "topK": 40                # Increased for better variety
        }
    }
    
    params = {"key": gemini_api_key}
    timeout = 15  # Increased timeout for better responses
    
    try:
        response = requests.post(GEMINI_API_URL, params=params, json=data, timeout=timeout)
        response.raise_for_status()
        resp_json = response.json()
        
        if "candidates" in resp_json and resp_json["candidates"]:
            parts = resp_json["candidates"][0].get("content", {}).get("parts", [])
            if parts and "text" in parts[0]:
                result = parts[0]["text"].strip()
                
                # Clean up the response - remove asterisks and format properly
                result = clean_response_formatting(result)
                
                # Increased response limit for better answers
                if len(result) > 1200:
                    result = result[:1200] + "..."
                
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
            return generate_intelligent_fallback(prompt, context)
        logger.error(f"API Error: {e.response.status_code}")
    except requests.exceptions.Timeout:
        logger.warning("Request timed out")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
    
    # Intelligent fallback
    return generate_intelligent_fallback(prompt, context)

def generate_intelligent_fallback(prompt: str, context: Optional[str] = None) -> str:
    """Generate intelligent fallback responses for legal questions"""
    prompt_lower = prompt.lower()
    
    # Common legal questions with comprehensive answers
    if any(word in prompt_lower for word in ['contract', 'contracts']):
        return """Contracts in Indian Law:

A contract is a legally binding agreement between two or more parties under the Indian Contract Act, 1872.

Essential Elements:
1. Offer and Acceptance: Clear proposal and unqualified acceptance
2. Consideration: Something of value exchanged (money, services, goods)
3. Capacity: Parties must be legally competent (major, sound mind)
4. Free Consent: Agreement without coercion, fraud, or misrepresentation
5. Lawful Object: Purpose must be legal and not against public policy

Types: Express, implied, executed, executory, valid, void, voidable, and unenforceable contracts.

Key Provisions: The Act covers performance, breach, remedies, and damages. Contracts can be discharged by performance, agreement, frustration, or breach."""
    
    if any(word in prompt_lower for word in ['chalan', 'challan']):
        return """Challan in Indian Legal Context:

A challan is an official document or receipt in India with multiple legal meanings:

1. Traffic Challan:
- Official notice for traffic violations
- Issued under Motor Vehicles Act, 1988
- Contains violation details, fine amount, and payment instructions
- Must be paid within specified time to avoid legal action

2. Court Challan:
- Document presenting an accused person before court
- Filed by police after investigation
- Contains charges and evidence summary

3. Tax/Customs Challan:
- Payment receipt for government taxes
- Used for income tax, customs duty, GST payments
- Serves as proof of tax compliance

Legal Implications: Non-payment of challans can lead to penalties, license suspension, or legal proceedings depending on the type."""
    
    if any(word in prompt_lower for word in ['termination', 'terminate']):
        return """Termination in Indian Contract Law:

Grounds for Termination:
1. Mutual Agreement: Both parties agree to end the contract
2. Breach: Material violation by one party
3. Frustration: Impossibility due to circumstances beyond control
4. Notice: As per contract terms or reasonable notice

Employment Termination:
- Governed by Industrial Disputes Act, 1947
- Shops and Establishments Acts (state-specific)
- Notice period requirements vary by position and state
- Wrongful termination can lead to compensation claims

Termination Clauses should specify:
- Notice period requirements
- Grounds for immediate termination
- Post-termination obligations
- Settlement of dues and benefits"""
    
    if any(word in prompt_lower for word in ['liability', 'indemnity']):
        return """Liability and Indemnity in Indian Law:

Types of Liability:
1. Contractual: Arising from breach of contract terms
2. Tortious: Civil wrongs causing harm or damage
3. Criminal: Violations of criminal law
4. Strict: Liability without fault (environmental, product liability)

Indemnity under Indian Contract Act:
- Section 124-125 governs indemnity contracts
- Indemnifier promises to compensate for loss/damage
- Indemnified party can recover actual damages
- Must be specific about scope and limitations

Key Considerations:
- Limitation of liability clauses
- Mutual vs. one-sided indemnity
- Insurance requirements
- Statutory limitations on liability exclusions"""
    
    if context and len(context) > 50 and not context.startswith("Unable to extract"):
        # Check if context contains PDF metadata or binary content
        if context.startswith("%PDF") or "obj" in context[:100] or "endobj" in context[:100]:
            return "I notice you've uploaded a PDF file, but I'm receiving the raw file data instead of extracted text. Please try uploading the PDF again, or if the issue persists, convert your document to a text format and try again."
        
        # Analyze the context to provide meaningful response
        if "education" in context.lower() or "university" in context.lower():
            return f"This appears to be an educational document/resume. While I can see it contains: {context[:200]}..., I'm specialized in legal document analysis. If you have legal questions or need to analyze legal documents, I'm here to help!"
        
        # General context-based response
        words = context.split()[:30]
        preview = ' '.join(words)
        return f"Based on your document content: {preview}... Please ask a specific question about legal aspects or upload a legal document for detailed analysis."
    
    # Default helpful response
    return "I'm here to help with Indian legal questions and document analysis. You can ask about contracts, legal procedures, Indian laws, or upload a legal document for analysis. What specific legal topic would you like to know about?"

# Keep the old function for backward compatibility
def generate_quick_fallback(prompt: str, context: Optional[str] = None) -> str:
    return generate_intelligent_fallback(prompt, context)
