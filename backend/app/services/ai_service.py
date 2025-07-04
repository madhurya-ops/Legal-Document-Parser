"""
AI Service for LegalDoc Application
Provides context-aware responses with source attribution for legal document analysis.
"""

import os
from typing import Dict, List, Optional, Tuple
import logging
from datetime import datetime

# Import the LLM client
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from llm.client import query

logger = logging.getLogger(__name__)

class AIService:
    """
    AI Service for providing context-aware legal assistance
    with source attribution and confidence scoring.
    """
    
    def __init__(self):
        self.system_message = os.environ.get(
            'AI_SERVICE_PROMPT',
            "You are a legal AI assistant specialized in Indian law. "
            "Provide accurate, helpful responses based on the context provided. "
            "Always cite sources when available and indicate confidence levels."
        )
    
    def generate_response(
        self, 
        user_query: str, 
        context: str = "", 
        sources: Optional[List[Dict]] = None,
        document_type: Optional[str] = None
    ) -> Dict:
        """
        Generate a context-aware response with source attribution.
        
        Args:
            user_query: The user's question or request
            context: Relevant document context
            sources: List of source documents with metadata
            document_type: Type of legal document being analyzed
            
        Returns:
            Dict containing response, sources, confidence score, and metadata
        """
        try:
            # Enhance the prompt with system message and context handling
            enhanced_prompt = self._build_enhanced_prompt(
                user_query, context, document_type
            )
            
            # Get response from LLM
            ai_response = query(context, enhanced_prompt)
            
            # Process and enhance the response
            processed_response = self._process_response(
                ai_response, sources, context
            )
            
            return processed_response
            
        except Exception as e:
            logger.error(f"Error generating AI response: {e}")
            return {
                "response": "I apologize, but I encountered an error processing your request. Please try again.",
                "confidence_score": 0.0,
                "sources": [],
                "citations": [],
                "metadata": {
                    "error": str(e),
                    "timestamp": datetime.now().isoformat()
                }
            }
    
    def _build_enhanced_prompt(
        self, 
        user_query: str, 
        context: str, 
        document_type: Optional[str]
    ) -> str:
        """Build an enhanced prompt with system instructions and context."""
        
        prompt_parts = [self.system_message]
        
        if document_type:
            prompt_parts.append(f"Document Type: {document_type}")
        
        if context:
            prompt_parts.append(f"Context Length: {len(context)} characters")
            prompt_parts.append("Please provide your response based on the provided context.")
        else:
            prompt_parts.append("No specific document context provided. Use your general legal knowledge.")
        
        prompt_parts.append(f"User Query: {user_query}")
        
        prompt_parts.extend([
            "Instructions:",
            "1. Provide accurate information based on the context",
            "2. Cite specific sections when referencing document content",
            "3. Indicate confidence level in your response",
            "4. Focus on Indian legal standards and practices",
            "5. If information is not available in context, clearly state this"
        ])
        
        return "\n\n".join(prompt_parts)
    
    def _process_response(
        self, 
        ai_response: str, 
        sources: Optional[List[Dict]], 
        context: str
    ) -> Dict:
        """Process the AI response and add metadata."""
        
        # Calculate confidence score
        confidence_score = self._calculate_confidence_score(ai_response, context)
        
        # Extract citations from response
        citations = self._extract_citations(ai_response)
        
        # Prepare source information
        source_info = self._prepare_source_info(sources)
        
        # Add response metadata
        metadata = {
            "response_length": len(ai_response),
            "context_length": len(context) if context else 0,
            "timestamp": datetime.now().isoformat(),
            "model": "gemini-1.5-flash",
            "has_context": bool(context),
            "source_count": len(source_info) if source_info else 0
        }
        
        return {
            "response": ai_response,
            "confidence_score": confidence_score,
            "sources": source_info,
            "citations": citations,
            "metadata": metadata
        }
    
    def _calculate_confidence_score(self, response: str, context: str) -> float:
        """Calculate confidence score based on response characteristics."""
        
        score = 0.5  # Base score
        
        # Increase score if context is available
        if context:
            score += 0.2
        
        # Increase score for longer, detailed responses
        if len(response) > 200:
            score += 0.1
        
        # Increase score if response contains specific legal terms
        legal_terms = [
            "section", "clause", "act", "regulation", "court", 
            "precedent", "case law", "statute", "provision"
        ]
        term_count = sum(1 for term in legal_terms if term.lower() in response.lower())
        score += min(term_count * 0.05, 0.2)
        
        # Decrease score for uncertainty indicators
        uncertainty_phrases = [
            "i don't know", "not sure", "uncertain", "unclear", 
            "might be", "possibly", "perhaps"
        ]
        uncertainty_count = sum(1 for phrase in uncertainty_phrases if phrase in response.lower())
        score -= min(uncertainty_count * 0.1, 0.3)
        
        # Ensure score is between 0 and 1
        return max(0.0, min(1.0, score))
    
    def _extract_citations(self, response: str) -> List[str]:
        """Extract potential citations from the response."""
        
        citations = []
        
        # Look for common citation patterns
        import re
        
        # Indian legal citation patterns
        patterns = [
            r'\(\d{4}\)\s+\d+\s+SCC\s+\d+',  # SCC citations
            r'AIR\s+\d{4}\s+SC\s+\d+',       # AIR citations
            r'Section\s+\d+',                # Section references
            r'Article\s+\d+',                # Article references
            r'Rule\s+\d+',                   # Rule references
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, response, re.IGNORECASE)
            citations.extend(matches)
        
        return list(set(citations))  # Remove duplicates
    
    def _prepare_source_info(self, sources: Optional[List[Dict]]) -> List[Dict]:
        """Prepare source information for response."""
        
        if not sources:
            return []
        
        source_info = []
        for source in sources:
            source_data = {
                "title": source.get("title", "Unknown Document"),
                "type": source.get("type", "Legal Document"),
                "relevance_score": source.get("relevance_score", 0.0),
                "page": source.get("page", 1),
                "section": source.get("section", "N/A")
            }
            source_info.append(source_data)
        
        return source_info

class LegalAnalysisService:
    """Specialized service for legal document analysis using AI."""
    
    def __init__(self):
        self.ai_service = AIService()
    
    def analyze_contract_terms(self, document_content: str, specific_terms: List[str] = None) -> Dict:
        """Analyze specific contract terms in a document."""
        
        terms_to_analyze = specific_terms or [
            "termination", "liability", "indemnification", "governing law", 
            "dispute resolution", "confidentiality", "intellectual property"
        ]
        
        query = f"Analyze the following contract terms in this document: {', '.join(terms_to_analyze)}. " \
                f"For each term, identify the relevant clauses, assess their fairness, and provide recommendations."
        
        return self.ai_service.generate_response(
            user_query=query,
            context=document_content,
            document_type="Contract"
        )
    
    def assess_compliance_risks(self, document_content: str, jurisdiction: str = "India") -> Dict:
        """Assess compliance risks in a legal document."""
        
        query = f"Assess the compliance risks in this document for {jurisdiction} jurisdiction. " \
                f"Identify potential regulatory violations, missing required clauses, and provide risk ratings."
        
        return self.ai_service.generate_response(
            user_query=query,
            context=document_content,
            document_type="Legal Document"
        )
    
    def extract_key_obligations(self, document_content: str) -> Dict:
        """Extract key obligations and responsibilities from a document."""
        
        query = "Extract and analyze all key obligations, responsibilities, and duties from this document. " \
                "Organize them by party and provide clear explanations of each obligation."
        
        return self.ai_service.generate_response(
            user_query=query,
            context=document_content,
            document_type="Legal Document"
        )
    
    def compare_documents(self, doc1_content: str, doc2_content: str) -> Dict:
        """Compare two legal documents and highlight differences."""
        
        combined_context = f"DOCUMENT 1:\n{doc1_content}\n\nDOCUMENT 2:\n{doc2_content}"
        
        query = "Compare these two legal documents and highlight key differences, similarities, " \
                "and any important changes between them. Focus on material changes that could " \
                "affect legal rights and obligations."
        
        return self.ai_service.generate_response(
            user_query=query,
            context=combined_context,
            document_type="Document Comparison"
        )

# Initialize services
ai_service = AIService()
legal_analysis_service = LegalAnalysisService()
