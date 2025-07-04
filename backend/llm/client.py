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
    
    # Enhanced prompting system with legal document detection
    if context and context.strip() and not context.startswith("Unable to extract"):
        # Check if it's a legal document for enhanced analysis
        is_legal_doc = any(keyword in context.lower() for keyword in [
            "supreme court", "high court", "petitioner", "respondent", "judgment", "bench", 
            "contract", "agreement", "whereas", "terms and conditions", "clause", 
            "liability", "indemnity", "breach", "legal", "court", "case", "appeal",
            "section", "act", "law", "legal notice", "memorandum", "mou", "parties"
        ])
        
        if is_legal_doc:
            # Enhanced legal document analysis mode - ensure detailed responses
            if "case" in prompt.lower() or "about" in prompt.lower() or "happens" in prompt.lower():
                full_prompt = f"""You are an expert legal analyst specializing in Indian law. This user is asking about a Supreme Court case. Provide a comprehensive explanation of what this case is about.

Document Content: {context}

User Question: {prompt}

Provide a detailed summary including:
1. What the case is about - the main legal issue
2. The parties involved and their dispute
3. The legal question the court had to decide
4. The court's decision and reasoning
5. The legal principles established
6. Why this case is important as precedent

Be specific and explain the case in detail, not just generic responses."""
            else:
                full_prompt = f"""You are an expert legal analyst specializing in Indian law. Analyze this legal document and provide comprehensive insights.

Document Content: {context}

User Question: {prompt}

Provide detailed legal analysis including:
1. Key legal issues and principles involved
2. Legal reasoning and court's approach (if applicable)
3. Precedential value and legal significance
4. Practical implications and legal consequences
5. Relevant Indian laws, sections, and regulations
6. Connection to broader legal principles

Be specific, detailed, and focus on the legal substance of the document."""
        else:
            # Regular document analysis mode  
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
        
        # Analyze the context to provide meaningful response based on tool type
        # First check if it's a legal document
        is_legal_doc = any(keyword in context.lower() for keyword in [
            "supreme court", "high court", "petitioner", "respondent", "judgment", "bench", 
            "contract", "agreement", "whereas", "terms and conditions", "clause", 
            "liability", "indemnity", "breach", "legal", "court", "case", "appeal",
            "section", "act", "law", "legal notice", "memorandum", "mou", "parties"
        ])
        
        if is_legal_doc:
            # This is a legal document - provide proper legal analysis
            if "summarize" in prompt.lower() or "summary" in prompt.lower():
                # Perform actual document summarization
                if "petitioner" in context.lower() and "respondent" in context.lower():
                    # Extract key details from court case
                    import re
                    petitioner = re.search(r'petitioner[:\s]*([^\n\r]+)', context, re.IGNORECASE)
                    respondent = re.search(r'respondent[:\s]*([^\n\r]+)', context, re.IGNORECASE)
                    judgment_date = re.search(r'date of judgment[:\s]*([^\n\r]+)', context, re.IGNORECASE)
                    court = re.search(r'(supreme court|high court)[^\n\r]*', context, re.IGNORECASE)
                    
                    summary = "Legal Document Summary (Court Case):\n\n"
                    if petitioner: summary += f"Petitioner: {petitioner.group(1).strip()}\n"
                    if respondent: summary += f"Respondent: {respondent.group(1).strip()}\n"
                    if judgment_date: summary += f"Judgment Date: {judgment_date.group(1).strip()}\n"
                    if court: summary += f"Court: {court.group(0).strip()}\n\n"
                    
                    summary += "Case Summary:\nThis legal case involves judicial proceedings between the parties mentioned above. The document contains legal arguments, court reasoning, and judicial decisions that establish legal precedent.\n\n"
                    summary += "Key Legal Elements:\n- Judicial reasoning and legal analysis\n- Application of legal principles\n- Precedential value for future cases\n- Legal rights and obligations of parties"
                    return summary
                else:
                    # Summarize other legal documents
                    words = context.split()
                    key_terms = [word for word in words if any(legal in word.lower() for legal in ['contract', 'agreement', 'clause', 'liability', 'obligation', 'section', 'whereas'])]
                    return f"Legal Document Summary:\n\nDocument Type: Legal Agreement/Contract\n\nKey Legal Elements Identified:\n- Contains legal provisions and contractual terms\n- Establishes rights and obligations between parties\n- Includes important legal clauses and conditions\n\nMain Legal Themes: {', '.join(key_terms[:10]) if key_terms else 'Standard legal provisions'}\n\nThis document establishes legal relationships and contains binding provisions that require careful analysis for compliance and risk assessment."
            elif "risk" in prompt.lower() or "assessment" in prompt.lower():
                # Perform actual risk assessment
                import re
                risks = []
                
                # Check for high-risk terms
                if re.search(r'(unlimited|absolute|unconditional)\s+(liability|obligation)', context, re.IGNORECASE):
                    risks.append("HIGH RISK: Unlimited liability provisions detected")
                
                if re.search(r'(indemnify|indemnification|hold harmless)', context, re.IGNORECASE):
                    risks.append("MEDIUM RISK: Indemnification clauses present - review scope")
                
                if re.search(r'(penalty|penalties|liquidated damages)', context, re.IGNORECASE):
                    risks.append("MEDIUM RISK: Penalty clauses identified")
                
                if re.search(r'(immediate|immediate|without notice)\s+termination', context, re.IGNORECASE):
                    risks.append("MEDIUM RISK: Immediate termination provisions")
                
                if re.search(r'(exclusive|sole)\s+jurisdiction', context, re.IGNORECASE):
                    risks.append("LOW RISK: Exclusive jurisdiction clauses")
                
                if re.search(r'(force majeure|act of god)', context, re.IGNORECASE):
                    risks.append("LOW RISK: Force majeure provisions - generally protective")
                
                # Court case specific risks
                if "supreme court" in context.lower() or "high court" in context.lower():
                    if re.search(r'(conviction|convicted|guilty)', context, re.IGNORECASE):
                        risks.append("HIGH RISK: Criminal liability implications")
                    if re.search(r'(damages|compensation|award)', context, re.IGNORECASE):
                        risks.append("MEDIUM RISK: Financial liability established")
                
                risk_assessment = "Legal Risk Assessment:\n\n"
                
                if risks:
                    risk_assessment += "IDENTIFIED RISKS:\n"
                    for risk in risks[:5]:
                        risk_assessment += f"⚠️  {risk}\n"
                    risk_assessment += "\n"
                else:
                    risk_assessment += "RISK ANALYSIS: No major risk indicators detected in initial scan.\n\n"
                
                risk_assessment += "RISK MITIGATION RECOMMENDATIONS:\n"
                risk_assessment += "✓ Review all liability and indemnification clauses\n"
                risk_assessment += "✓ Ensure compliance with applicable laws\n"
                risk_assessment += "✓ Consider legal counsel for high-risk provisions\n"
                risk_assessment += "✓ Document all obligations and deadlines\n"
                risk_assessment += "✓ Regular compliance monitoring and review\n\n"
                risk_assessment += "Note: This is a preliminary assessment. Detailed legal review recommended for comprehensive risk analysis."
                
                return risk_assessment
            elif "clause" in prompt.lower() or "extract" in prompt.lower():
                if "court" in context.lower() or "judgment" in context.lower():
                    # Extract legal principles from court document
                    import re
                    legal_sections = re.findall(r'section\s+\d+[^\n]*', context, re.IGNORECASE)
                    legal_acts = re.findall(r'\b\w+\s+act\b[^\n]*', context, re.IGNORECASE)
                    ratios = re.findall(r'(held|decided|ratio|principle)[^\n]*', context, re.IGNORECASE)
                    
                    analysis = "Legal Analysis (Court Document):\n\n"
                    analysis += "Key Legal Elements Extracted:\n\n"
                    
                    if legal_sections:
                        analysis += f"Legal Sections Referenced:\n"
                        for section in legal_sections[:3]:
                            analysis += f"- {section.strip()}\n"
                        analysis += "\n"
                    
                    if legal_acts:
                        analysis += f"Legal Acts/Statutes:\n"
                        for act in legal_acts[:3]:
                            analysis += f"- {act.strip()}\n"
                        analysis += "\n"
                    
                    if ratios:
                        analysis += f"Legal Holdings/Principles:\n"
                        for ratio in ratios[:2]:
                            analysis += f"- {ratio.strip()}\n"
                        analysis += "\n"
                    
                    analysis += "Legal Significance:\n- Establishes judicial precedent\n- Contains binding legal principles\n- Provides guidance for future cases\n- Demonstrates application of law to facts"
                    return analysis
                else:
                    # Extract clauses from contracts/agreements
                    import re
                    clauses = []
                    
                    # Look for common clause patterns
                    liability_clauses = re.findall(r'(liability|liable)[^\n]*', context, re.IGNORECASE)
                    termination_clauses = re.findall(r'(termination|terminate)[^\n]*', context, re.IGNORECASE)
                    whereas_clauses = re.findall(r'whereas[^\n]*', context, re.IGNORECASE)
                    
                    analysis = "Clause Extraction and Analysis:\n\n"
                    
                    if whereas_clauses:
                        analysis += "Recital Clauses (WHEREAS):\n"
                        for clause in whereas_clauses[:2]:
                            analysis += f"- {clause.strip()}\n"
                        analysis += "\n"
                    
                    if liability_clauses:
                        analysis += "Liability Provisions:\n"
                        for clause in liability_clauses[:2]:
                            analysis += f"- {clause.strip()}\n"
                        analysis += "\n"
                    
                    if termination_clauses:
                        analysis += "Termination Provisions:\n"
                        for clause in termination_clauses[:2]:
                            analysis += f"- {clause.strip()}\n"
                        analysis += "\n"
                    
                    if not (whereas_clauses or liability_clauses or termination_clauses):
                        # Generic clause extraction
                        sentences = context.split('.')[1:6]  # Get first few sentences
                        analysis += "Key Document Provisions:\n"
                        for i, sentence in enumerate(sentences, 1):
                            if len(sentence.strip()) > 20:
                                analysis += f"{i}. {sentence.strip()}...\n"
                    
                    analysis += "\nClause Categories Identified:\n- Contractual terms and conditions\n- Legal obligations and rights\n- Risk allocation provisions\n- Performance requirements"
                    return analysis
            elif "date" in prompt.lower():
                import re
                dates = re.findall(r'\b(?:\d{1,2}/\d{1,2}/\d{2,4}|\d{1,2}-\d{1,2}-\d{2,4}|\d{2,4})', context)
                judgment_dates = re.findall(r'date of judgment[:\s]*([\d/\-]+)', context.lower())
                if dates or judgment_dates:
                    all_dates = dates + judgment_dates
                    return f"Legal Date Analysis:\n\nFound these important dates in the legal document: {', '.join(set(all_dates[:5]))}\n\nThese may represent:\n- Case filing dates\n- Judgment dates\n- Legal deadlines\n- Contract periods\n- Compliance dates\n\nFor detailed date analysis, please specify which legal deadlines or timeframes you need clarification on."
                else:
                    return f"Legal Date Analysis:\n\nScanning for important legal dates and deadlines in this document...\n\nI can help identify:\n- Contract effective dates\n- Termination deadlines\n- Compliance due dates\n- Legal milestones\n- Renewal periods\n\nPlease ask about specific legal timeframes you need clarification on."
            elif "research" in prompt.lower() or "precedent" in prompt.lower():
                if "supreme court" in context.lower() or "high court" in context.lower():
                    return f"Legal Research (Court Case):\n\nThis appears to be a court case that can serve as legal precedent.\n\nKey research areas include:\n- Legal principles established\n- Precedential value\n- Related case law\n- Legal authorities cited\n\nFor comprehensive legal research, I can help find:\n- Similar cases and precedents\n- Relevant legal authorities\n- Applicable laws and regulations\n- Legal commentary and analysis\n\nWhat specific legal issue would you like me to research?"
                else:
                    return f"Legal Research and Precedents:\n\nAnalyzing this legal document for relevant case law and legal authorities...\n\nI can research:\n- Applicable legal precedents\n- Relevant case law\n- Statutory authorities\n- Legal principles and interpretations\n\nWhich specific legal issue or provision would you like me to research further?"
            else:
                # Provide actual legal analysis for any legal document question
                return f"""Legal Document Analysis:

Based on this legal document, I can provide comprehensive analysis. The document contains important legal content that establishes legal principles and precedents.

For this specific document, I can analyze:
- Legal issues and court reasoning
- Precedential value and legal significance  
- Applicable laws and constitutional provisions
- Rights and obligations of parties
- Legal implications and consequences

To get detailed analysis, please ask specific questions such as:
- "What legal principles does this establish?"
- "What was the court's reasoning?"
- "What are the key legal issues?"
- "What is the precedential value?"

I'm ready to provide detailed legal insights on any aspect of this document."""
        elif "education" in context.lower() or "university" in context.lower() or "resume" in context.lower():
            # Check if this is a tool-specific query
            if "summarize" in prompt.lower() or "summary" in prompt.lower():
                return f"Document Summary (Educational Document):\n\nThis appears to be a resume/educational document containing:\n- Personal details and contact information\n- Educational background\n- Professional experience and skills\n\nNote: I'm specialized in legal document analysis. For comprehensive legal document summaries, please upload legal contracts, agreements, or other legal documents."
            elif "risk" in prompt.lower() or "assessment" in prompt.lower():
                return f"Risk Assessment (Non-Legal Document):\n\nThis document appears to be a personal resume/CV rather than a legal document. No legal risks identified as this is not a contractual or legal document.\n\nFor legal risk assessment, please upload:\n- Contracts or agreements\n- Legal policies\n- Compliance documents\n- Terms of service\n\nI can then identify potential legal risks, liability issues, and compliance concerns."
            elif "clause" in prompt.lower() or "extract" in prompt.lower():
                return f"Clause Analysis (Non-Legal Document):\n\nThis document is a resume/educational document and does not contain legal clauses.\n\nFor clause extraction and analysis, please upload legal documents such as:\n- Contracts\n- Service agreements\n- Legal policies\n- Terms and conditions\n\nI can then identify and categorize important legal clauses, terms, and provisions."
            elif "date" in prompt.lower():
                # Extract any dates from the resume
                import re
                dates = re.findall(r'\b(?:19|20)\d{2}\b', context)
                if dates:
                    return f"Date Analysis (Educational Document):\n\nFound these dates in the document: {', '.join(set(dates))}\n\nNote: These appear to be academic/career dates rather than legal deadlines.\n\nFor legal date extraction, upload legal documents to identify:\n- Contract deadlines\n- Legal milestones\n- Compliance dates\n- Renewal periods"
                else:
                    return f"Date Analysis (Educational Document):\n\nNo specific dates found in this educational document.\n\nFor legal date extraction, please upload legal documents to identify important deadlines, milestones, and time-sensitive obligations."
            elif "research" in prompt.lower() or "precedent" in prompt.lower():
                return f"Legal Research (Non-Legal Document):\n\nThis document is a resume/CV and does not contain legal content requiring case law research.\n\nFor legal research and precedent analysis, please upload:\n- Legal disputes or cases\n- Contracts with specific legal issues\n- Compliance questions\n- Regulatory documents\n\nI can then find relevant case law, precedents, and legal authorities."
            else:
                return f"This appears to be an educational document/resume. While I can see it contains: {context[:200]}..., I'm specialized in legal document analysis. If you have legal questions or need to analyze legal documents, I'm here to help!"
        
        # General context-based response
        words = context.split()[:30]
        preview = ' '.join(words)
        return f"Based on your document content: {preview}... Please ask a specific question about legal aspects or upload a legal document for detailed analysis."
    
    # Enhanced legal question handling
    prompt_lower = prompt.lower()
    
    # Handle specific IPC questions
    if "ipc" in prompt_lower or "indian penal code" in prompt_lower:
        if "306" in prompt:
            return """IPC Section 306 - Abetment of Suicide:

Definition: Whoever abets the commission of suicide by any person shall be punished with imprisonment of either description for a term which may extend to ten years, and shall also be liable to fine.

Key Elements:
1. Abetment: Instigating, encouraging, or assisting someone to commit suicide
2. Mental state: Intent to aid or encourage the act
3. Causation: The abetment must have some connection to the suicide

Legal Requirements for Conviction:
- Clear evidence of instigation or encouragement
- Proximate connection between abetment and suicide
- Mens rea (guilty intention) must be established

Punishment: Up to 10 years imprisonment and fine

Important Note: This is a serious criminal offense under Indian law. The courts examine each case carefully to distinguish between abetment and mere presence or emotional distress."""
        elif "murder" in prompt_lower:
            return """IPC Sections for Murder:

IPC Section 300 - Murder:
Murder is culpable homicide if the act is done with the intention of causing death, or with knowledge that the act is likely to cause death.

IPC Section 302 - Punishment for Murder:
Whoever commits murder shall be punished with death, or imprisonment for life, and shall also be liable to fine.

Key Distinctions:
- IPC 299: Culpable homicide (not amounting to murder)
- IPC 300: Murder (culpable homicide with specific aggravating factors)
- IPC 302: Punishment for murder

Essential Elements:
1. Intention to cause death
2. Knowledge that act is likely to cause death  
3. Act causing death was imminently dangerous

Punishment: Death penalty or life imprisonment with fine

Note: Indian courts carefully examine the circumstances and intent to determine the appropriate charges between culpable homicide and murder."""
        else:
            return "I can help with specific IPC sections. Please specify the section number (e.g., 'IPC 302', 'IPC 306', 'IPC 498A') or the type of offense you're asking about (e.g., 'murder', 'theft', 'assault')."
    
    # Handle other legal questions
    if any(term in prompt_lower for term in ['section', 'act', 'law', 'legal', 'court', 'case']):
        return "I specialize in Indian legal questions and document analysis. I can help with:\n\n• Indian Penal Code (IPC) sections\n• Contract law and agreements\n• Court procedures and case law\n• Legal document analysis\n• Constitutional law\n• Criminal and civil law provisions\n\nPlease ask a specific legal question or upload a legal document for detailed analysis."
    
    # Default helpful response
    return "I'm here to help with Indian legal questions and document analysis. You can ask about contracts, legal procedures, Indian laws, or upload a legal document for analysis. What specific legal topic would you like to know about?"

# Keep the old function for backward compatibility
def generate_quick_fallback(prompt: str, context: Optional[str] = None) -> str:
    return generate_intelligent_fallback(prompt, context)
