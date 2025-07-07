"""
AI Service for LegalDoc Application
Provides context-aware responses with source attribution for legal document analysis.
Enhanced for comprehensive legal analysis without token limitations.
Built to provide genuine value to legal professionals.
"""

import os
import re
import random
from typing import Dict, List, Optional, Tuple, Union
import logging
from datetime import datetime, timedelta
import httpx
import asyncio
import json
from enum import Enum

from ..core.config import get_settings

logger = logging.getLogger(__name__)

class DocumentType(Enum):
    """Enum for document types to ensure consistent handling"""
    COURT_JUDGMENT = "court_judgment"
    CONTRACT = "contract"
    LEGAL_NOTICE = "legal_notice"
    PETITION = "petition"
    AGREEMENT = "agreement"
    COMPLIANCE_DOCUMENT = "compliance_document"
    LEGAL_OPINION = "legal_opinion"
    STATUTE = "statute"
    REGULATION = "regulation"
    CASE_LAW = "case_law"
    UNKNOWN = "unknown"

class LegalDomain(Enum):
    """Legal practice areas for specialized analysis"""
    CORPORATE = "corporate_law"
    LITIGATION = "litigation"
    CONTRACTS = "contract_law"
    INTELLECTUAL_PROPERTY = "intellectual_property"
    TAXATION = "taxation"
    LABOR_EMPLOYMENT = "labor_employment"
    REAL_ESTATE = "real_estate"
    FAMILY = "family_law"
    CRIMINAL = "criminal_law"
    CONSTITUTIONAL = "constitutional_law"
    REGULATORY = "regulatory_law"
    GENERAL = "general_practice"

def get_greeting() -> str:
    """Generate appropriate greeting based on time of day with Indian touch"""
    hour = datetime.now().hour
    if 5 <= hour < 12:
        return random.choice(["Namaste! ", "Shubh prabhat! ", "Good morning! "])
    elif 12 <= hour < 17:
        return random.choice(["Namaste! ", "Shubh dina! ", "Good afternoon! "])
    else:
        return random.choice(["Namaste! ", "Shubh sandhya! ", "Good evening! "])

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
    result = re.sub(r' +', ' ', result)
    
    return result.strip()

class AIService:
    """
    Enhanced AI Service for providing context-aware legal assistance
    with source attribution and confidence scoring.
    Built specifically for legal professionals with practical, actionable insights.
    """
    
    def __init__(self):
        settings = get_settings()
        self.system_message = getattr(settings, 'AI_SERVICE_PROMPT', None) or (
            "You are an expert legal AI assistant specialized in Indian law with deep expertise across "
            "multiple practice areas. Provide comprehensive, accurate, and actionable legal analysis. "
            "Always cite sources, provide structured responses, and offer practical recommendations "
            "that lawyers can immediately use in their practice."
        )
        
        # Enhanced API configuration with fallback support
        self.primary_api_key = getattr(settings, 'GEMINI_API_KEY', None) or os.environ.get('GEMINI_API_KEY')
        
        # Optional fallback keys - only add if they exist
        potential_fallback_keys = [
            getattr(settings, 'GEMINI_API_KEY_2', None) or os.environ.get('GEMINI_API_KEY_2'),
            getattr(settings, 'GEMINI_API_KEY_3', None) or os.environ.get('GEMINI_API_KEY_3'),
            getattr(settings, 'GEMINI_API_KEY_4', None) or os.environ.get('GEMINI_API_KEY_4'),
        ]
        # Filter out None values and placeholder values
        self.fallback_api_keys = [
            key for key in potential_fallback_keys 
            if key and key.strip() and not key.startswith('your_') and len(key.strip()) > 10
        ]
        
        self.gemini_api_url = getattr(settings, 'GEMINI_API_URL', None) or os.environ.get(
            'GEMINI_API_URL',
            "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"
        )
        
        # Validate primary API key
        if self.primary_api_key and self.primary_api_key.startswith('your_'):
            self.primary_api_key = None
        
        # API key usage tracking for intelligent fallback
        self.api_key_status = {}
        
        if self.primary_api_key:
            self.api_key_status['primary'] = {
                'key': self.primary_api_key, 
                'rate_limit_reset': None, 
                'failed_attempts': 0
            }
        
        for i, key in enumerate(self.fallback_api_keys):
            self.api_key_status[f'fallback_{i+1}'] = {
                'key': key, 'rate_limit_reset': None, 'failed_attempts': 0
            }
        
        # Check if we have at least one valid API key
        if not self.primary_api_key and not self.fallback_api_keys:
            logger.warning("No valid Gemini API keys found. Please set GEMINI_API_KEY environment variable.")
            self.has_valid_keys = False
        else:
            total_keys = (1 if self.primary_api_key else 0) + len(self.fallback_api_keys)
            logger.info(f"AI service initialized with {total_keys} valid API key(s)")
            self.has_valid_keys = True
        
        # Enhanced caching and analytics
        self.response_cache = {}
        self.usage_analytics = {
            'total_queries': 0,
            'successful_queries': 0,
            'cache_hits': 0,
            'api_failures': 0,
            'fallback_usage': 0
        }
    
    def get_available_api_key(self) -> Optional[str]:
        """Get the next available API key, considering rate limits and failures."""
        current_time = datetime.now()
        
        # Check primary key first
        primary_status = self.api_key_status['primary']
        if (primary_status['key'] and 
            (not primary_status['rate_limit_reset'] or current_time > primary_status['rate_limit_reset']) and
            primary_status['failed_attempts'] < 3):
            return primary_status['key']
        
        # Check fallback keys
        for key_name, status in self.api_key_status.items():
            if key_name.startswith('fallback_'):
                if (status['key'] and 
                    (not status['rate_limit_reset'] or current_time > status['rate_limit_reset']) and
                    status['failed_attempts'] < 3):
                    return status['key']
        
        # If all keys are rate limited or failed, return the primary (it might work)
        return self.primary_api_key
    
    def mark_api_key_rate_limited(self, api_key: str, reset_time_minutes: int = 60):
        """Mark an API key as rate limited with reset time."""
        reset_time = datetime.now() + timedelta(minutes=reset_time_minutes)
        
        for key_name, status in self.api_key_status.items():
            if status['key'] == api_key:
                status['rate_limit_reset'] = reset_time
                status['failed_attempts'] += 1
                logger.warning(f"API key {key_name} rate limited. Reset time: {reset_time}")
                break
    
    def mark_api_key_failed(self, api_key: str):
        """Mark an API key as failed."""
        for key_name, status in self.api_key_status.items():
            if status['key'] == api_key:
                status['failed_attempts'] += 1
                if status['failed_attempts'] >= 3:
                    logger.error(f"API key {key_name} has failed {status['failed_attempts']} times")
                break
    
    def reset_api_key_status(self, api_key: str):
        """Reset API key status after successful use."""
        for key_name, status in self.api_key_status.items():
            if status['key'] == api_key:
                status['failed_attempts'] = 0
                status['rate_limit_reset'] = None
                break

    async def generate_response(
        self, 
        user_query: str, 
        context: str = "", 
        sources: Optional[List[Dict]] = None,
        document_type: Optional[str] = None,
        legal_domain: Optional[str] = None
    ) -> Dict:
        """
        Generate a comprehensive context-aware response with source attribution.
        Enhanced for detailed legal analysis providing genuine value to lawyers.
        
        Args:
            user_query: The user's question or request
            context: Relevant document context
            sources: List of source documents with metadata
            document_type: Type of legal document being analyzed
            legal_domain: Legal practice area for specialized analysis
            
        Returns:
            Dict containing detailed response, sources, confidence score, and actionable insights
        """
        self.usage_analytics['total_queries'] += 1
        
        try:
            # Handle simple greetings without API call
            prompt_lower = user_query.lower().strip()
            if self._is_simple_greeting(prompt_lower):
                return self._generate_greeting_response()
            
            # Generate cache key for performance optimization
            cache_key = hash((user_query[:100], context[:500] if context else "", document_type, legal_domain))
            if cache_key in self.response_cache:
                self.usage_analytics['cache_hits'] += 1
                logger.info("Returning cached response")
                return self.response_cache[cache_key]
            
            # Detect document type and legal domain if not provided
            if not document_type:
                document_type = self._detect_document_type(context).value
            if not legal_domain:
                legal_domain = self._detect_legal_domain(user_query, context).value
            
            # Enhanced prompt building for practical legal analysis
            enhanced_prompt = self._build_lawyer_focused_prompt(
                user_query, context, document_type, legal_domain
            )
            
            # Get detailed response from LLM with fallback support
            ai_response = await self._query_gemini_api_with_fallback(enhanced_prompt)
            
            # Process and enhance the response with practical legal insights
            processed_response = self._process_lawyer_focused_response(
                ai_response, sources, context, user_query, document_type, legal_domain
            )
            
            # Cache successful responses (limit cache size)
            self.response_cache[cache_key] = processed_response
            if len(self.response_cache) > 150:  # Increased cache size
                # Remove oldest entries
                keys_to_remove = list(self.response_cache.keys())[:30]
                for key in keys_to_remove:
                    del self.response_cache[key]
            
            self.usage_analytics['successful_queries'] += 1
            return processed_response
            
        except Exception as e:
            logger.error(f"Error generating AI response: {e}")
            self.usage_analytics['api_failures'] += 1
            return self._generate_comprehensive_fallback_response(user_query, context, str(e))
    
    async def _query_gemini_api_with_fallback(self, prompt: str) -> str:
        """Query the Gemini API with intelligent fallback support for rate limits."""
        
        # Try primary and fallback keys
        for attempt in range(len(self.api_key_status)):
            api_key = self.get_available_api_key()
            
            if not api_key:
                logger.warning("No available API keys, using intelligent fallback")
                self.usage_analytics['fallback_usage'] += 1
                return self._generate_intelligent_fallback(prompt)
            
            try:
                result = await self._make_gemini_api_call(api_key, prompt)
                if result:
                    self.reset_api_key_status(api_key)
                    return result
                    
            except Exception as e:
                if "429" in str(e) or "quota" in str(e).lower() or "rate limit" in str(e).lower():
                    logger.warning(f"Rate limit hit for API key, trying next key")
                    self.mark_api_key_rate_limited(api_key)
                else:
                    logger.error(f"API call failed: {e}")
                    self.mark_api_key_failed(api_key)
                
                # Continue to next API key
                continue
        
        # All API keys failed, use intelligent fallback
        logger.warning("All API keys exhausted, using intelligent fallback")
        self.usage_analytics['fallback_usage'] += 1
        return self._generate_intelligent_fallback(prompt)
    
    async def _make_gemini_api_call(self, api_key: str, prompt: str) -> Optional[str]:
        """Make the actual API call to Gemini."""
        
        # Enhanced API call configuration for professional legal responses
        data = {
            "contents": [{
                "role": "user",
                "parts": [{
                    "text": prompt
                }]
            }],
            "generationConfig": {
                "maxOutputTokens": 8192,  # Maximum for detailed legal analysis
                "temperature": 0.2,      # Lower for more factual, professional responses
                "topP": 0.85,           # Balanced for legal precision
                "topK": 25,             # More focused responses
                "stopSequences": ["###END###", "---STOP---"]  # Clear stop indicators
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
        
        params = {"key": api_key}
        timeout = 90  # Increased timeout for complex legal analysis
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.gemini_api_url, 
                params=params, 
                json=data, 
                timeout=timeout
            )
            response.raise_for_status()
            resp_json = response.json()
            
            if "candidates" in resp_json and resp_json["candidates"]:
                parts = resp_json["candidates"][0].get("content", {}).get("parts", [])
                if parts and "text" in parts[0]:
                    result = parts[0]["text"].strip()
                    
                    # Clean up the response
                    result = clean_response_formatting(result)
                    
                    # Ensure comprehensive response (minimal truncation for lawyers)
                    if len(result) > 15000:  # Only truncate if extremely long
                        result = result[:15000] + "\n\n[Response truncated due to length - please ask for specific sections for complete analysis]"
                    
                    return result
            
            # If we get here, response format was unexpected
            logger.error(f"Unexpected response format: {resp_json}")
            return None

    def _detect_document_type(self, context: str) -> DocumentType:
        """Detect document type based on content analysis."""
        if not context:
            return DocumentType.UNKNOWN
            
        context_lower = context.lower()
        
        # Court document indicators
        if any(keyword in context_lower for keyword in [
            "supreme court", "high court", "district court", "tribunal", 
            "petitioner", "respondent", "judgment", "order", "decree",
            "in the matter of", "versus", "vs.", "writ petition", "civil appeal"
        ]):
            return DocumentType.COURT_JUDGMENT
        
        # Contract indicators
        if any(keyword in context_lower for keyword in [
            "agreement", "contract", "party", "parties", "clause", "term", 
            "whereas", "witnesseth", "indemnity", "liability", "breach",
            "warranty", "confidentiality", "governing law", "jurisdiction"
        ]):
            return DocumentType.CONTRACT
        
        # Legal notice indicators
        if any(keyword in context_lower for keyword in [
            "legal notice", "notice under section", "under provisions of", 
            "demand notice", "cease and desist", "caused this notice to be issued",
            "through advocate", "drawn on behalf of", "client instructions"
        ]):
            return DocumentType.LEGAL_NOTICE
        
        return DocumentType.UNKNOWN

    def _detect_legal_domain(self, query: str, context: str) -> LegalDomain:
        """Detect the legal practice area for specialized analysis."""
        combined_text = (query + " " + context).lower()
        
        # Corporate law indicators
        if any(term in combined_text for term in [
            "company", "corporation", "merger", "acquisition", "shares", "board", 
            "directors", "shareholders", "corporate governance", "compliance", "securities"
        ]):
            return LegalDomain.CORPORATE
        
        # Contract law indicators
        if any(term in combined_text for term in [
            "agreement", "contract", "breach", "damages", "performance", "obligation", 
            "warranty", "indemnity", "termination", "consideration"
        ]):
            return LegalDomain.CONTRACTS
        
        # Litigation indicators
        if any(term in combined_text for term in [
            "lawsuit", "litigation", "court", "judge", "trial", "evidence", 
            "witness", "testimony", "pleading", "motion", "appeal"
        ]):
            return LegalDomain.LITIGATION
        
        # IP law indicators
        if any(term in combined_text for term in [
            "patent", "trademark", "copyright", "intellectual property", "infringement", 
            "license", "royalty", "trade secret", "brand"
        ]):
            return LegalDomain.INTELLECTUAL_PROPERTY
        
        # Tax law indicators
        if any(term in combined_text for term in [
            "tax", "income tax", "gst", "customs", "excise", "assessment", 
            "refund", "penalty", "tribunal", "revenue"
        ]):
            return LegalDomain.TAXATION
        
        # Labor law indicators
        if any(term in combined_text for term in [
            "employment", "employee", "employer", "wages", "termination", 
            "discrimination", "harassment", "union", "labor", "workplace"
        ]):
            return LegalDomain.LABOR_EMPLOYMENT
        
        # Real estate indicators
        if any(term in combined_text for term in [
            "property", "real estate", "land", "lease", "rent", "mortgage", 
            "title", "deed", "zoning", "development"
        ]):
            return LegalDomain.REAL_ESTATE
        
        # Criminal law indicators
        if any(term in combined_text for term in [
            "criminal", "crime", "arrest", "police", "bail", "custody", 
            "prosecution", "defense", "sentence", "conviction"
        ]):
            return LegalDomain.CRIMINAL
        
        # Constitutional law indicators
        if any(term in combined_text for term in [
            "constitution", "fundamental rights", "directive principles", 
            "amendment", "judicial review", "federalism", "separation of powers"
        ]):
            return LegalDomain.CONSTITUTIONAL
        
        return LegalDomain.GENERAL

    def _build_lawyer_focused_prompt(
        self, 
        user_query: str, 
        context: str, 
        document_type: str,
        legal_domain: str
    ) -> str:
        """Build a lawyer-focused prompt for practical legal analysis."""
        
        greeting = get_greeting()
        prompt_lower = user_query.lower().strip()
        
        # All legal questions should hit the API - no more generic fallbacks
        
        # Domain-specific analysis based on detected legal area
        domain_specific_instructions = self._get_domain_specific_instructions(legal_domain)
        
        if context and context.strip() and not context.startswith("Unable to extract"):
            if document_type == "court_judgment":
                return f"""{greeting}You are a senior litigation specialist. Analyze this court judgment with focus on practical legal implications.

DOCUMENT CONTENT:
{context[:25000]}

LAWYER'S QUESTION:
{user_query if user_query else 'Provide comprehensive judgment analysis'}

REQUIRED ANALYSIS:
1. **Case Summary**: Parties, court hierarchy, case type, and key issues
2. **Legal Holdings**: Primary legal principles established (ratio decidendi)
3. **Precedential Value**: Binding nature and jurisdictional scope
4. **Practice Implications**: How this affects similar cases and legal strategy
5. **Citation Format**: Proper legal citation for future reference
6. **Key Quotable Passages**: Important judicial observations for arguments
7. **Distinguishing Factors**: Elements that might limit precedential scope
8. **Strategic Insights**: How lawyers can use this judgment in practice

{domain_specific_instructions}

Provide actionable insights that lawyers can immediately apply in their practice."""
                
            elif document_type == "contract":
                return f"""{greeting}You are a senior contracts specialist. Analyze this agreement with focus on risk assessment and practical recommendations.

DOCUMENT CONTENT:
{context[:25000]}

LAWYER'S QUESTION:
{user_query if user_query else 'Provide comprehensive contract analysis'}

REQUIRED ANALYSIS:
1. **Contract Structure**: Type, parties, governing law, and jurisdiction
2. **Key Commercial Terms**: Payment, performance obligations, and deliverables
3. **Risk Assessment**: Major legal and commercial risks identified
4. **Problematic Clauses**: Unfavorable or ambiguous terms requiring attention
5. **Missing Protections**: Important clauses that should be added
6. **Termination Rights**: Exit mechanisms and consequences
7. **Dispute Resolution**: Mechanisms and potential issues
8. **Negotiation Points**: Specific terms to renegotiate for better protection
9. **Compliance Requirements**: Regulatory obligations and deadlines
10. **Enforcement Issues**: Potential challenges in enforcement

{domain_specific_instructions}

Focus on actionable recommendations for contract negotiation and risk mitigation."""
                
            elif document_type == "legal_notice":
                return f"""{greeting}You are a senior litigation counsel. Analyze this legal notice and provide strategic response guidance.

DOCUMENT CONTENT:
{context[:25000]}

LAWYER'S QUESTION:
{user_query if user_query else 'Provide strategic analysis and response guidance'}

REQUIRED ANALYSIS:
1. **Notice Analysis**: Type, legal basis, and claims made
2. **Legal Merit Assessment**: Strength of opponent's legal position
3. **Response Timeline**: Critical deadlines and response requirements
4. **Defense Strategy**: Potential defenses and counter-arguments
5. **Evidence Requirements**: Documents and proof needed for defense
6. **Settlement Considerations**: Whether and how to negotiate settlement
7. **Counter-Notice Options**: Potential for counter-claims or defensive notices
8. **Cost-Benefit Analysis**: Litigation costs vs. settlement prospects
9. **Procedural Next Steps**: Immediate actions required
10. **Risk Mitigation**: Steps to minimize exposure and strengthen position

{domain_specific_instructions}

Provide specific, actionable guidance for responding to this notice effectively."""
            
            else:
                # Generic legal document analysis
                return f"""{greeting}You are a senior legal consultant. Analyze this document and provide comprehensive legal insights.

DOCUMENT CONTENT:
{context[:25000]}

LAWYER'S QUESTION:
{user_query}

ANALYSIS FRAMEWORK:
1. **Document Classification**: Type, purpose, and legal significance
2. **Legal Framework**: Applicable laws, regulations, and precedents
3. **Rights and Obligations**: Analysis of parties' legal positions
4. **Compliance Assessment**: Regulatory requirements and gaps
5. **Risk Identification**: Legal, commercial, and operational risks
6. **Actionable Recommendations**: Specific steps for legal compliance
7. **Strategic Considerations**: Broader implications for client's business
8. **Documentation Needs**: Additional documents or evidence required

{domain_specific_instructions}

Provide practical, implementable recommendations that add immediate value to legal practice."""
        else:
            # General legal question without document context
            return f"""{greeting}You are a senior legal advisor specializing in Indian law. Provide comprehensive, actionable guidance.

LEGAL QUESTION:
{user_query}

RESPONSE FRAMEWORK:
1. **Direct Answer**: Clear, authoritative response to the question
2. **Legal Authority**: Relevant statutes, rules, and case law with citations
3. **Practical Application**: How this applies in real-world scenarios
4. **Procedural Steps**: Specific actions required for implementation
5. **Timeline Considerations**: Critical deadlines and timing issues
6. **Documentation Requirements**: Forms, applications, or evidence needed
7. **Potential Challenges**: Common obstacles and how to address them
8. **Alternative Approaches**: Different strategies or options available
9. **Cost Implications**: Fee structures, court costs, or financial considerations
10. **Best Practices**: Professional recommendations for optimal outcomes

{domain_specific_instructions}

Structure your response for immediate practical application by legal professionals."""

    def _get_domain_specific_instructions(self, legal_domain: str) -> str:
        """Get specialized instructions based on legal domain."""
        
        domain_instructions = {
            "corporate_law": """
CORPORATE LAW FOCUS:
- Analyze board resolutions, shareholder agreements, and compliance requirements
- Identify Companies Act 2013 implications and regulatory filing obligations
- Assess corporate governance risks and best practices
- Review director liabilities and indemnification provisions
- Consider SEBI regulations for listed companies""",
            
            "litigation": """
LITIGATION FOCUS:
- Evaluate evidence strength and procedural compliance
- Identify grounds for appeals or revisions
- Assess limitation periods and jurisdictional issues
- Consider interim relief and protective measures
- Analyze cost implications and recovery prospects""",
            
            "contract_law": """
CONTRACT LAW FOCUS:
- Review performance obligations and breach consequences
- Assess enforceability and void/voidable provisions
- Consider Indian Contract Act 1872 implications
- Evaluate dispute resolution and governing law clauses
- Identify force majeure and termination scenarios""",
            
            "intellectual_property": """
IP LAW FOCUS:
- Analyze trademark, patent, and copyright implications
- Review licensing terms and royalty structures
- Assess infringement risks and enforcement options
- Consider IP registration and prosecution strategies
- Evaluate trade secret protection measures""",
            
            "taxation": """
TAXATION FOCUS:
- Analyze income tax, GST, and regulatory compliance
- Review tax planning strategies and optimization opportunities
- Assess penalty and prosecution risks
- Consider appeal procedures and settlement options
- Evaluate transfer pricing and international tax implications""",
            
            "labor_employment": """
EMPLOYMENT LAW FOCUS:
- Review employment contracts and service conditions
- Analyze termination procedures and notice requirements
- Assess compliance with labor laws and factory acts
- Consider provident fund, ESI, and statutory benefits
- Evaluate workplace policies and disciplinary procedures""",
            
            "real_estate": """
REAL ESTATE FOCUS:
- Analyze property titles and encumbrance certificates
- Review sale deeds, lease agreements, and development agreements
- Assess RERA compliance and approvals
- Consider stamp duty, registration, and tax implications
- Evaluate zoning laws and land use restrictions""",
        }
        
        return domain_instructions.get(legal_domain, "")

    def _process_lawyer_focused_response(
        self, 
        ai_response: str, 
        sources: Optional[List[Dict]], 
        context: str,
        user_query: str,
        document_type: str,
        legal_domain: str
    ) -> Dict:
        """Process the AI response and add lawyer-focused metadata and insights."""
        
        # Calculate enhanced confidence score for legal analysis
        confidence_score = self._calculate_professional_confidence_score(
            ai_response, context, user_query, document_type, legal_domain
        )
        
        # Extract comprehensive legal citations
        citations = self._extract_comprehensive_legal_citations(ai_response)
        
        # Prepare enhanced source information
        source_info = self._prepare_professional_source_info(sources, context)
        
        # Generate actionable insights for lawyers
        actionable_insights = self._generate_actionable_insights(
            ai_response, document_type, legal_domain, user_query
        )
        
        # Generate comprehensive metadata
        metadata = {
            "response_length": len(ai_response),
            "context_length": len(context) if context else 0,
            "timestamp": datetime.now().isoformat(),
            "model": "gemini-1.5-flash-enhanced",
            "has_context": bool(context),
            "source_count": len(source_info) if source_info else 0,
            "document_type": document_type,
            "legal_domain": legal_domain,
            "query_classification": self._classify_lawyer_query_type(user_query),
            "analysis_depth": "comprehensive",
            "professional_grade": True,
            "citation_count": len(citations),
            "actionable_items": len(actionable_insights)
        }
        
        return {
            "response": ai_response,
            "confidence_score": confidence_score,
            "sources": source_info,
            "citations": citations,
            "actionable_insights": actionable_insights,
            "metadata": metadata
        }

    def _calculate_professional_confidence_score(
        self, response: str, context: str, query: str, doc_type: str, legal_domain: str
    ) -> float:
        """Calculate confidence score optimized for legal professional use."""
        
        score = 0.7  # Higher base score for professional system
        
        # Context quality bonus
        if context:
            score += 0.15
            if len(context) > 2000:  # Substantial legal document
                score += 0.1
        
        # Response comprehensiveness
        if len(response) > 800:  # Detailed legal analysis
            score += 0.1
        if len(response) > 2000:  # Very comprehensive analysis
            score += 0.05
        
        # Legal terminology and structure
        professional_indicators = [
            "section", "clause", "provision", "precedent", "case law", "statute",
            "regulation", "compliance", "liability", "jurisdiction", "appeal",
            "evidence", "procedure", "remedy", "enforcement", "tribunal"
        ]
        term_score = sum(1 for term in professional_indicators if term.lower() in response.lower())
        score += min(term_score * 0.02, 0.12)
        
        # Structured analysis indicators
        structure_markers = [
            "analysis:", "recommendation:", "conclusion:", "next steps:",
            "1.", "2.", "3.", "•", "risk:", "consideration:", "note:"
        ]
        structure_score = sum(1 for marker in structure_markers if marker.lower() in response.lower())
        score += min(structure_score * 0.015, 0.08)
        
        # Domain-specific expertise bonus
        if legal_domain != "general_practice":
            score += 0.05
        
        # Reduce score for uncertainty (but minimal penalty for professional hedging)
        uncertainty_phrases = ["unclear", "uncertain", "might be", "possibly", "perhaps"]
        uncertainty_count = sum(1 for phrase in uncertainty_phrases if phrase in response.lower())
        score -= min(uncertainty_count * 0.03, 0.1)
        
        # Query relevance bonus
        if query and any(word in response.lower() for word in query.lower().split()[:5]):
            score += 0.03
        
        return max(0.3, min(1.0, score))  # Professional minimum of 0.3
    
    def _is_simple_greeting(self, prompt_lower: str) -> bool:
        """Check if the prompt is just a simple greeting or small talk."""
        greeting_words = ['hello', 'hi', 'hey', 'namaste', 'namaskar', 'good morning', 'good afternoon', 'good evening']
        small_talk = ['how are you', 'what is your name', 'who are you', 'what can you do']
        
        # Check if the entire prompt is just a greeting
        if prompt_lower in greeting_words:
            return True
            
        # Check if it's basic small talk
        if any(talk in prompt_lower for talk in small_talk):
            return True
            
        # If prompt is very short and contains only greeting words
        words = prompt_lower.split()
        if len(words) <= 3 and all(word in greeting_words for word in words):
            return True
            
        return False
    
    def _generate_greeting_response(self) -> Dict:
        """Generate a simple greeting response without API call."""
        greeting = get_greeting()
        response = f"""{greeting}I'm your AI legal assistant specialized in Indian law. I can help you with:

• Legal document analysis and review
• Case law research and precedent analysis
• Contract drafting and risk assessment
• Compliance and regulatory guidance
• Legal strategy and recommendations

Please ask me any legal question or upload a document for analysis."""
        
        return {
            "response": response,
            "confidence_score": 1.0,
            "sources": [],
            "citations": [],
            "actionable_insights": [],
            "metadata": {
                "response_type": "greeting",
                "timestamp": datetime.now().isoformat(),
                "model": "greeting_handler",
                "professional_grade": True
            }
        }

    def _extract_comprehensive_legal_citations(self, response: str) -> List[str]:
        """Extract comprehensive legal citations optimized for Indian legal practice."""
        
        citations = []
        
        # Enhanced Indian legal citation patterns
        patterns = [
            r'\(\d{4}\)\s+\d+\s+SCC\s+\d+',           # SCC citations
            r'AIR\s+\d{4}\s+SC\s+\d+',                # AIR Supreme Court
            r'AIR\s+\d{4}\s+[A-Z]+\s+\d+',            # AIR High Courts
            r'\d{4}\s+\(\d+\)\s+SCC\s+\d+',          # Alternative SCC format
            r'Section\s+\d+[A-Z]*(\(\d+\))?',         # Section references with sub-sections
            r'Article\s+\d+[A-Z]*',                   # Constitutional articles
            r'Rule\s+\d+[A-Z]*',                      # Rule references
            r'Chapter\s+[IVX]+',                      # Chapter references
            r'Schedule\s+[IVX]+',                     # Schedule references
            r'\b[A-Z][a-z]+\s+Act,?\s+\d{4}',         # Act names with year
            r'\b[A-Z][a-z]+\s+Code\b',                # Code references
            r'Order\s+[IVX]+\s+Rule\s+\d+',          # CPC/CrPC references
            r'Regulation\s+\d+',                      # Regulation references
            r'Clause\s+\d+[a-z]*',                    # Clause references
            r'Para\s+\d+',                            # Paragraph references
            r'Proviso\s+to\s+Section\s+\d+',          # Proviso references
            r'\b\d{4}\s+SCC\s+\([A-Z]+\)\s+\d+',     # SCC with note references
            r'MANU/[A-Z]+/\d+/\d+',                  # MANU citations
            r'\(\d{4}\)\s+\d+\s+SCR\s+\d+',          # SCR citations
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, response, re.IGNORECASE)
            citations.extend(matches)
        
        # Extract case names (enhanced for Indian naming conventions)
        case_patterns = [
            r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\s+[Vv]\.?\s+[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b',
            r'\bState\s+of\s+[A-Z][a-z]+\s+[Vv]\.?\s+[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b',
            r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\s+[Vv]\.?\s+Union\s+of\s+India\b'
        ]
        
        for pattern in case_patterns:
            case_matches = re.findall(pattern, response)
            citations.extend(case_matches)
        
        # Remove duplicates and clean up
        unique_citations = list(set(citations))
        return [citation.strip() for citation in unique_citations if len(citation.strip()) > 3]

    def _generate_actionable_insights(
        self, response: str, doc_type: str, legal_domain: str, query: str
    ) -> List[Dict]:
        """Generate actionable insights for lawyers based on the analysis."""
        
        insights = []
        
        # Extract action items from response
        action_patterns = [
            r'(?:should|must|need to|recommend|suggest|advise)\s+([^.]+)',
            r'(?:next step|action|procedure):\s*([^.]+)',
            r'(?:consider|review|examine)\s+([^.]+)',
        ]
        
        for pattern in action_patterns:
            matches = re.findall(pattern, response, re.IGNORECASE)
            for match in matches[:3]:  # Limit to top 3 per pattern
                insights.append({
                    "type": "action_item",
                    "description": match.strip(),
                    "priority": "medium",
                    "category": "procedural"
                })
        
        # Domain-specific insights
        if legal_domain == "litigation":
            insights.append({
                "type": "deadline_alert",
                "description": "Review limitation periods and filing deadlines",
                "priority": "high",
                "category": "compliance"
            })
        elif legal_domain == "contracts":
            insights.append({
                "type": "risk_assessment",
                "description": "Conduct thorough due diligence on counterparty",
                "priority": "medium",
                "category": "risk_management"
            })
        elif legal_domain == "corporate_law":
            insights.append({
                "type": "compliance_check",
                "description": "Ensure board resolutions and regulatory filings are current",
                "priority": "high",
                "category": "compliance"
            })
        
        # Document-specific insights
        if doc_type == "court_judgment":
            insights.append({
                "type": "precedent_analysis",
                "description": "Analyze precedential value for similar cases",
                "priority": "medium",
                "category": "legal_research"
            })
        elif doc_type == "legal_notice":
            insights.append({
                "type": "response_strategy",
                "description": "Prepare comprehensive response within statutory timeline",
                "priority": "high",
                "category": "litigation_strategy"
            })
        
        return insights[:5]  # Limit to top 5 insights

    def _classify_lawyer_query_type(self, query: str) -> str:
        """Classify query type for legal professional context."""
        query_lower = query.lower()
        
        if any(word in query_lower for word in ['analyze', 'analysis', 'review']):
            return "document_analysis"
        elif any(word in query_lower for word in ['risk', 'risks', 'assess', 'assessment']):
            return "risk_assessment"
        elif any(word in query_lower for word in ['strategy', 'approach', 'recommend']):
            return "strategic_advice"
        elif any(word in query_lower for word in ['compliance', 'regulatory', 'legal requirement']):
            return "compliance_inquiry"
        elif any(word in query_lower for word in ['precedent', 'case law', 'citation']):
            return "legal_research"
        elif any(word in query_lower for word in ['draft', 'drafting', 'agreement', 'contract']):
            return "document_drafting"
        elif any(word in query_lower for word in ['procedure', 'process', 'steps']):
            return "procedural_inquiry"
        else:
            return "general_legal_inquiry"

    def _prepare_professional_source_info(self, sources: Optional[List[Dict]], context: str = "") -> List[Dict]:
        """Prepare enhanced source information for legal professionals."""
        
        source_info = []
        
        # Add provided sources with professional metadata
        if sources:
            for source in sources:
                source_data = {
                    "title": source.get("title", "Legal Document"),
                    "type": source.get("type", "Primary Source"),
                    "relevance_score": source.get("relevance_score", 0.0),
                    "page": source.get("page", 1),
                    "section": source.get("section", "N/A"),
                    "confidence": source.get("confidence", "high"),
                    "authority_level": source.get("authority_level", "primary"),
                    "jurisdiction": source.get("jurisdiction", "India"),
                    "legal_weight": source.get("legal_weight", "binding")
                }
                source_info.append(source_data)
        
        # Add context-derived source with professional classification
        if context:
            context_source = {
                "title": "Analyzed Document",
                "type": "Primary Legal Document",
                "relevance_score": 1.0,
                "page": 1,
                "section": "Complete Document",
                "confidence": "high",
                "content_length": len(context),
                "analysis_type": "comprehensive_legal_analysis",
                "authority_level": "primary",
                "jurisdiction": "India",
                "legal_weight": "binding"
            }
            source_info.append(context_source)
        
        return source_info

    def _generate_comprehensive_fallback_response(self, user_query: str, context: str, error: str) -> Dict:
        """Generate comprehensive fallback response when API fails."""
        greeting = get_greeting()
        
        if context and len(context) > 100:
            # Intelligent context analysis for fallback
            fallback_response = f"""{greeting}I'm experiencing technical difficulties but can provide preliminary insights based on the document content.

DOCUMENT ASSESSMENT:
{self._extract_professional_context_summary(context)}

IMMEDIATE RECOMMENDATIONS:
1. Review the document for key legal provisions and obligations
2. Identify critical deadlines and compliance requirements
3. Consult with domain experts for specialized analysis
4. Prepare comprehensive documentation for legal review

NEXT STEPS:
- Please try your query again in a few moments
- For urgent matters, consider consulting the original source documents
- Break complex questions into specific focused inquiries

I apologize for the technical difficulty. The system is designed to provide comprehensive legal analysis and will be fully operational shortly."""
        else:
            fallback_response = f"""{greeting}I'm experiencing technical difficulties but remain committed to providing comprehensive legal assistance.

AVAILABLE SERVICES:
- Document analysis and review
- Legal research and precedent analysis
- Risk assessment and compliance checking
- Strategic legal advice and recommendations
- Contract review and drafting support

IMMEDIATE ASSISTANCE:
1. Try rephrasing your question with specific focus areas
2. Break complex queries into discrete legal issues
3. Ensure documents are in supported formats (PDF, DOCX, TXT)
4. For urgent matters, consult primary legal sources

TECHNICAL ISSUE:
This appears to be a temporary service interruption. The system includes multiple fallback mechanisms and should resume full operation shortly.

I'm designed specifically for legal professionals and will provide comprehensive, actionable analysis once the technical issue is resolved."""
        
        return {
            "response": fallback_response,
            "confidence_score": 0.4,  # Higher than generic fallback
            "sources": [],
            "citations": [],
            "actionable_insights": [
                {
                    "type": "system_status",
                    "description": "Retry query after technical issue resolution",
                    "priority": "medium",
                    "category": "system"
                }
            ],
            "metadata": {
                "error": error,
                "timestamp": datetime.now().isoformat(),
                "fallback": True,
                "model": "intelligent_fallback_system",
                "professional_grade": True
            }
        }

    def _extract_professional_context_summary(self, context: str) -> str:
        """Extract professional summary from context for fallback responses."""
        try:
            # Extract meaningful legal content
            sentences = context.split('.')[:5]  # First 5 sentences
            legal_content = '. '.join(s.strip() for s in sentences if len(s.strip()) > 30)
            
            if legal_content:
                return f"Document contains legal provisions requiring professional analysis: {legal_content[:400]}..."
            else:
                return "Document contains legal text requiring comprehensive professional review and analysis."
        except:
            return "Legal document identified requiring professional legal analysis and expert review."

    def _generate_intelligent_fallback(self, prompt: str) -> str:
        """Generate intelligent fallback responses for various legal queries."""
        prompt_lower = prompt.lower()
        greeting = get_greeting()
        
        # Advanced pattern-based responses for lawyers
        if any(word in prompt_lower for word in ['judgment', 'court', 'case', 'precedent']):
            return f"""{greeting}I specialize in comprehensive court judgment analysis for legal professionals.

JUDGMENT ANALYSIS SERVICES:
1. **Precedential Value Assessment**: Determining binding authority and jurisdictional scope
2. **Ratio Decidendi Extraction**: Identifying core legal principles established
3. **Case Distinguishment**: Analyzing factual and legal distinctions for arguments
4. **Appeal Prospects**: Evaluating grounds for appellate review
5. **Strategic Application**: How to leverage the judgment in practice

For complete analysis, please ensure the judgment document is uploaded in a supported format. I provide detailed insights that lawyers can immediately apply in litigation strategy and case preparation."""
        
        elif any(word in prompt_lower for word in ['contract', 'agreement', 'clause', 'breach']):
            return f"""{greeting}I provide comprehensive contract analysis tailored for legal practitioners.

CONTRACT ANALYSIS CAPABILITIES:
1. **Risk Assessment Matrix**: Identifying and quantifying legal and commercial risks
2. **Clause-by-Clause Review**: Detailed analysis of terms and conditions
3. **Negotiation Strategy**: Specific points for improving client protection
4. **Enforcement Analysis**: Practical considerations for contract enforcement
5. **Compliance Mapping**: Regulatory requirements and obligations

Upload your contract document for detailed analysis including risk mitigation strategies, negotiation recommendations, and enforcement considerations."""
        
        elif any(word in prompt_lower for word in ['notice', 'legal notice', 'demand']):
            return f"""{greeting}I provide strategic legal notice analysis and response guidance.

LEGAL NOTICE SERVICES:
1. **Merit Assessment**: Evaluating the legal strength of claims made
2. **Response Strategy**: Comprehensive approach to legal response
3. **Defense Identification**: Potential defenses and counter-arguments
4. **Settlement Analysis**: Cost-benefit evaluation of settlement vs. litigation
5. **Procedural Compliance**: Ensuring proper legal response procedures

For strategic guidance, upload the legal notice for detailed analysis of response options and litigation risk assessment."""
        
        else:
            return f"""{greeting}I'm a comprehensive legal AI designed specifically for legal professionals practicing in India.

CORE CAPABILITIES:
**Document Analysis**: Court judgments, contracts, legal notices, regulatory documents
**Legal Research**: Case law analysis, precedent research, statutory interpretation
**Risk Assessment**: Legal and commercial risk identification and mitigation
**Strategic Advice**: Litigation strategy, negotiation tactics, compliance planning
**Professional Support**: Drafting assistance, due diligence, regulatory compliance

**Practice Areas**: Corporate Law, Litigation, Contracts, IP, Taxation, Employment Law, Real Estate

Please retry your query or upload relevant documents for comprehensive legal analysis. I'm designed to provide actionable insights that enhance legal practice efficiency and effectiveness."""

    async def get_usage_analytics(self) -> Dict:
        """Get usage analytics for monitoring and optimization."""
        return {
            "analytics": self.usage_analytics.copy(),
            "api_key_status": {
                key: {
                    "available": bool(status['key']),
                    "failed_attempts": status['failed_attempts'],
                    "rate_limited": bool(status['rate_limit_reset'] and 
                                      datetime.now() < status['rate_limit_reset'])
                } for key, status in self.api_key_status.items()
            },
            "cache_size": len(self.response_cache),
            "timestamp": datetime.now().isoformat()
        }


class LegalAnalysisService:
    """Specialized service for comprehensive legal document analysis using enhanced AI."""
    
    def __init__(self):
        self.ai_service = AIService()
    
    async def analyze_contract_terms(
        self, 
        document_content: str, 
        specific_terms: List[str] = None
    ) -> Dict:
        """Analyze specific contract terms with lawyer-focused insights."""
        
        query = "Analyze the key contract terms and identify risks, obligations, and recommendations."
        if specific_terms:
            query += f" Pay special attention to: {', '.join(specific_terms)}"
        
        return await self.ai_service.generate_response(
            user_query=query,
            context=document_content,
            document_type="contract",
            legal_domain="contracts"
        )
    
    async def assess_litigation_risk(
        self, 
        document_content: str, 
        case_context: str = ""
    ) -> Dict:
        """Assess litigation risks with strategic recommendations."""
        
        query = f"Assess litigation risks and provide strategic recommendations. Context: {case_context}"
        
        return await self.ai_service.generate_response(
            user_query=query,
            context=document_content,
            document_type="legal_notice",
            legal_domain="litigation"
        )
    
    async def analyze_compliance_requirements(
        self, 
        document_content: str, 
        regulatory_domain: str = ""
    ) -> Dict:
        """Analyze compliance requirements with actionable steps."""
        
        query = f"Analyze compliance requirements and identify necessary actions for {regulatory_domain} domain."
        
        return await self.ai_service.generate_response(
            user_query=query,
            context=document_content,
            document_type="compliance_document",
            legal_domain="regulatory_law"
        )

    async def extract_legal_precedents(
        self, 
        judgment_content: str, 
        case_similarity: str = ""
    ) -> Dict:
        """Extract legal precedents and analyze their application."""
        
        query = f"Extract legal precedents and analyze their precedential value. Focus on similarity to: {case_similarity}"
        
        return await self.ai_service.generate_response(
            user_query=query,
            context=judgment_content,
            document_type="court_judgment",
            legal_domain="litigation"
        )

# Create service instances
ai_service = AIService()
legal_analysis_service = LegalAnalysisService()
