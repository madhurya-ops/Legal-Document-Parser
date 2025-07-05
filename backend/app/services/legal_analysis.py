from typing import Dict, List, Any, Optional
import re
import os
import sys

# Add the parent directory to the path to import llm.client
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from ..schemas import ClauseExtractionResponse, ComplianceCheckResponse, PrecedentSearchResponse

try:
    from llm.client import query
except ImportError:
    # Fallback import if the module structure is different
    def query(context: str, prompt: str) -> str:
        return "Legal analysis service is currently unavailable. Please check the Gemini API configuration."

class ClauseExtractor:
    """Service for extracting and analyzing legal clauses from documents"""
    
    CLAUSE_TYPES = {
        "termination": ["termination", "terminate", "end", "expiry", "expire"],
        "indemnity": ["indemnity", "indemnification", "liable", "liability", "damages"],
        "jurisdiction": ["jurisdiction", "governing law", "court", "dispute resolution"],
        "force_majeure": ["force majeure", "act of god", "unforeseeable", "extraordinary"],
        "confidentiality": ["confidential", "non-disclosure", "proprietary", "secret"],
        "payment": ["payment", "fee", "compensation", "remuneration", "salary"],
        "intellectual_property": ["intellectual property", "copyright", "trademark", "patent"],
        "non_compete": ["non-compete", "non-competition", "restraint of trade"],
        "arbitration": ["arbitration", "arbitrator", "alternative dispute resolution"]
    }
    
    def extract_clauses(self, document_content: str, document_id: Optional[str] = None) -> ClauseExtractionResponse:
        """Extract legal clauses from document content"""
        
        # Use AI to identify and extract clauses
        prompt = f"""
        Analyze the following legal document and extract key clauses. Focus on Indian legal standards and practices.

        Document Content:
        {document_content[:3000]}  # Limit content to avoid token limits

        Extract and analyze the following types of clauses:
        1. TERMINATION CLAUSES - How and when the agreement can be terminated
        2. INDEMNITY CLAUSES - Who is liable for what damages or losses
        3. JURISDICTION CLAUSES - Which courts have jurisdiction, governing law
        4. FORCE MAJEURE CLAUSES - Unforeseeable circumstances provisions
        5. CONFIDENTIALITY CLAUSES - Non-disclosure and proprietary information
        6. PAYMENT CLAUSES - Payment terms, schedules, penalties
        7. INTELLECTUAL PROPERTY CLAUSES - IP ownership and usage rights
        8. NON-COMPETE CLAUSES - Restraint of trade provisions
        9. ARBITRATION CLAUSES - Dispute resolution mechanisms

        For each clause found, provide:
        - The exact text of the clause
        - Risk level (High/Medium/Low)
        - Explanation of potential issues
        - Recommendations for improvement

        If a clause type is missing, note it as "Not Found" and recommend adding it.

        Format your response as a structured analysis with clear sections for each clause type.
        """
        
        ai_response = query("", prompt)
        
        # Parse AI response and extract structured data
        clauses = self._parse_clause_response(ai_response)
        confidence_scores = self._calculate_confidence_scores(clauses)
        risk_assessment = self._assess_risks(clauses)
        recommendations = self._generate_recommendations(clauses, document_content)
        
        return ClauseExtractionResponse(
            clauses=clauses,
            confidence_scores=confidence_scores,
            risk_assessment=risk_assessment,
            recommendations=recommendations
        )
    
    def _parse_clause_response(self, ai_response: str) -> List[Dict[str, Any]]:
        """Parse AI response into structured clause data"""
        clauses = []
        
        # Basic parsing - in production, this would be more sophisticated
        for clause_type in self.CLAUSE_TYPES.keys():
            clause_data = {
                "type": clause_type,
                "text": "",
                "risk_level": "Unknown",
                "explanation": "",
                "found": False
            }
            
            # Search for clause mentions in AI response
            if clause_type.replace("_", " ") in ai_response.lower():
                clause_data["found"] = True
                clause_data["risk_level"] = self._extract_risk_level(ai_response, clause_type)
                clause_data["explanation"] = self._extract_explanation(ai_response, clause_type)
            
            clauses.append(clause_data)
        
        return clauses
    
    def _extract_risk_level(self, response: str, clause_type: str) -> str:
        """Extract risk level for a clause from AI response"""
        # Simple pattern matching - could be improved with NLP
        context = self._get_clause_context(response, clause_type)
        
        if any(word in context.lower() for word in ["high risk", "problematic", "concerning", "missing"]):
            return "High"
        elif any(word in context.lower() for word in ["medium risk", "moderate", "review"]):
            return "Medium"
        else:
            return "Low"
    
    def _extract_explanation(self, response: str, clause_type: str) -> str:
        """Extract explanation for a clause from AI response"""
        context = self._get_clause_context(response, clause_type)
        # Return first few sentences that mention the clause
        sentences = context.split('. ')
        relevant_sentences = [s for s in sentences if clause_type.replace("_", " ") in s.lower()]
        return '. '.join(relevant_sentences[:2]) if relevant_sentences else "No specific explanation found."
    
    def _get_clause_context(self, response: str, clause_type: str) -> str:
        """Get relevant context for a clause type from the response"""
        lines = response.split('\n')
        clause_name = clause_type.replace("_", " ").title()
        
        for i, line in enumerate(lines):
            if clause_name in line or clause_type in line.lower():
                # Return this line and next few lines as context
                context_lines = lines[i:i+5]
                return ' '.join(context_lines)
        
        return ""
    
    def _calculate_confidence_scores(self, clauses: List[Dict[str, Any]]) -> Dict[str, float]:
        """Calculate confidence scores for extracted clauses"""
        scores = {}
        for clause in clauses:
            # Simple scoring based on whether clause was found and has explanation
            if clause["found"] and clause["explanation"]:
                scores[clause["type"]] = 0.8
            elif clause["found"]:
                scores[clause["type"]] = 0.6
            else:
                scores[clause["type"]] = 0.3
        return scores
    
    def _assess_risks(self, clauses: List[Dict[str, Any]]) -> Dict[str, str]:
        """Assess overall risks based on extracted clauses"""
        risk_counts = {"High": 0, "Medium": 0, "Low": 0}
        
        for clause in clauses:
            risk_level = clause.get("risk_level", "Unknown")
            if risk_level in risk_counts:
                risk_counts[risk_level] += 1
        
        # Determine overall risk
        if risk_counts["High"] > 2:
            overall_risk = "High - Multiple high-risk clauses identified"
        elif risk_counts["High"] > 0 or risk_counts["Medium"] > 3:
            overall_risk = "Medium - Some concerning clauses found"
        else:
            overall_risk = "Low - Most clauses appear standard"
        
        missing_clauses = [c["type"] for c in clauses if not c["found"]]
        
        return {
            "overall_risk": overall_risk,
            "high_risk_count": risk_counts["High"],
            "medium_risk_count": risk_counts["Medium"],
            "missing_clauses": ", ".join(missing_clauses) if missing_clauses else "None"
        }
    
    def _generate_recommendations(self, clauses: List[Dict[str, Any]], document_content: str) -> List[str]:
        """Generate recommendations based on clause analysis"""
        recommendations = []
        
        # Check for missing critical clauses
        missing_critical = [c for c in clauses if not c["found"] and c["type"] in ["termination", "jurisdiction", "indemnity"]]
        if missing_critical:
            recommendations.append(f"Add missing critical clauses: {', '.join([c['type'] for c in missing_critical])}")
        
        # Check for high-risk clauses
        high_risk = [c for c in clauses if c["risk_level"] == "High"]
        if high_risk:
            recommendations.append("Review and revise high-risk clauses identified above")
        
        # Document length check
        if len(document_content) < 1000:
            recommendations.append("Document appears brief - consider adding more detailed terms and conditions")
        
        # Generic recommendations
        recommendations.extend([
            "Have the document reviewed by a qualified legal professional",
            "Ensure compliance with applicable Indian laws and regulations",
            "Consider adding dispute resolution mechanisms if not present"
        ])
        
        return recommendations


class ComplianceChecker:
    """Service for checking regulatory compliance"""
    
    INDIAN_REGULATIONS = {
        "companies_act": "Companies Act, 2013",
        "sebi": "SEBI Regulations",
        "fdi": "Foreign Direct Investment Policy",
        "employment": "Employment Laws (Shops and Establishments Act, etc.)",
        "contract": "Indian Contract Act, 1872",
        "ip": "Intellectual Property Laws",
        "data_protection": "Personal Data Protection Act (Proposed)"
    }
    
    def check_compliance(self, document_content: str, jurisdiction: str = "india", document_id: Optional[str] = None) -> ComplianceCheckResponse:
        """Check document compliance with relevant regulations"""
        
        prompt = f"""
        Review the following legal document for compliance with Indian laws and regulations.

        Document Content:
        {document_content[:3000]}

        Check compliance with:
        1. Indian Contract Act, 1872
        2. Companies Act, 2013 (if corporate document)
        3. SEBI Regulations (if securities/investment related)
        4. Employment Laws (if employment contract)
        5. FDI Policy (if foreign investment involved)
        6. Intellectual Property Laws
        7. Consumer Protection Act
        8. Data Protection considerations

        For each regulation:
        - Identify if it applies to this document
        - Check for compliance issues
        - Note missing required clauses
        - Assess compliance risk level

        Provide specific recommendations for ensuring compliance.
        """
        
        ai_response = query("", prompt)
        
        # Parse compliance analysis
        compliance_status = self._determine_compliance_status(ai_response)
        missing_clauses = self._extract_missing_clauses(ai_response)
        regulatory_requirements = self._extract_regulatory_requirements(ai_response)
        recommendations = self._extract_compliance_recommendations(ai_response)
        confidence_score = self._calculate_compliance_confidence(ai_response)
        
        return ComplianceCheckResponse(
            compliance_status=compliance_status,
            missing_clauses=missing_clauses,
            regulatory_requirements=regulatory_requirements,
            recommendations=recommendations,
            confidence_score=confidence_score
        )
    
    def _determine_compliance_status(self, ai_response: str) -> str:
        """Determine overall compliance status from AI response"""
        response_lower = ai_response.lower()
        
        if any(word in response_lower for word in ["non-compliant", "violations", "serious issues"]):
            return "Non-Compliant"
        elif any(word in response_lower for word in ["partially compliant", "some issues", "minor violations"]):
            return "Partially Compliant"
        elif any(word in response_lower for word in ["compliant", "meets requirements", "satisfactory"]):
            return "Compliant"
        else:
            return "Requires Review"
    
    def _extract_missing_clauses(self, ai_response: str) -> List[str]:
        """Extract missing clauses from AI response"""
        missing_clauses = []
        
        # Look for patterns indicating missing clauses
        lines = ai_response.split('\n')
        for line in lines:
            if "missing" in line.lower() or "add" in line.lower() or "required" in line.lower():
                if any(word in line.lower() for word in ["clause", "provision", "term"]):
                    missing_clauses.append(line.strip())
        
        return missing_clauses[:5]  # Limit to top 5
    
    def _extract_regulatory_requirements(self, ai_response: str) -> List[Dict[str, Any]]:
        """Extract regulatory requirements from AI response"""
        requirements = []
        
        for reg_key, reg_name in self.INDIAN_REGULATIONS.items():
            if reg_name.lower() in ai_response.lower() or reg_key in ai_response.lower():
                requirements.append({
                    "regulation": reg_name,
                    "applicable": True,
                    "status": "Requires Review",
                    "description": f"Document may be subject to {reg_name} requirements"
                })
        
        return requirements
    
    def _extract_compliance_recommendations(self, ai_response: str) -> List[str]:
        """Extract compliance recommendations from AI response"""
        recommendations = []
        
        # Look for recommendation patterns
        lines = ai_response.split('\n')
        for line in lines:
            if any(word in line.lower() for word in ["recommend", "should", "must", "ensure", "consider"]):
                if len(line.strip()) > 10:  # Avoid very short lines
                    recommendations.append(line.strip())
        
        # Add default recommendations
        recommendations.extend([
            "Consult with a legal expert familiar with Indian regulations",
            "Regular compliance reviews should be conducted",
            "Stay updated with regulatory changes"
        ])
        
        return recommendations[:8]  # Limit to reasonable number
    
    def _calculate_compliance_confidence(self, ai_response: str) -> float:
        """Calculate confidence score for compliance analysis"""
        # Simple scoring based on response detail and specific mentions
        score = 0.5  # Base score
        
        if len(ai_response) > 500:  # Detailed response
            score += 0.2
        
        regulation_mentions = sum(1 for reg in self.INDIAN_REGULATIONS.values() if reg.lower() in ai_response.lower())
        score += min(regulation_mentions * 0.1, 0.2)
        
        if "compliant" in ai_response.lower():
            score += 0.1
        
        return min(score, 0.9)  # Cap at 0.9


class PrecedentEngine:
    """Service for finding relevant legal precedents"""
    
    def find_relevant_precedents(self, query: str, jurisdiction: str = "india", document_type: Optional[str] = None) -> PrecedentSearchResponse:
        """Find relevant legal precedents for the given query"""
        
        # In a production system, this would query actual legal databases
        # For now, we'll use AI to suggest relevant precedents
        
        prompt = f"""
        Find relevant Indian legal precedents for the following query:
        Query: {query}
        Jurisdiction: {jurisdiction}
        Document Type: {document_type or "General"}

        Provide information about:
        1. Relevant Supreme Court cases
        2. High Court decisions
        3. Legal principles established
        4. How these precedents apply to the query
        5. Citation format for each case

        Focus on cases that are:
        - From Indian courts (Supreme Court, High Courts)
        - Relevant to the legal issue in the query
        - Recent and still valid precedents
        - Widely cited and authoritative

        Format each precedent with proper legal citation.
        """
        
        ai_response = query("", prompt)
        
        # Parse precedent information
        precedents = self._parse_precedents(ai_response)
        relevance_scores = self._calculate_relevance_scores(precedents, query)
        citations = self._extract_citations(precedents)
        
        return PrecedentSearchResponse(
            precedents=precedents,
            relevance_scores=relevance_scores,
            citations=citations
        )
    
    def _parse_precedents(self, ai_response: str) -> List[Dict[str, Any]]:
        """Parse AI response to extract precedent information"""
        precedents = []
        
        # Split response into potential case sections
        sections = ai_response.split('\n\n')
        
        for section in sections:
            if any(word in section for word in ['v.', 'vs.', 'Supreme Court', 'High Court', 'AIR', 'SCC']):
                precedent = {
                    "case_name": self._extract_case_name(section),
                    "court": self._extract_court(section),
                    "year": self._extract_year(section),
                    "citation": self._extract_citation(section),
                    "legal_principle": self._extract_principle(section),
                    "relevance": self._extract_relevance(section),
                    "summary": section[:200] + "..." if len(section) > 200 else section
                }
                
                if precedent["case_name"]:  # Only add if we found a case name
                    precedents.append(precedent)
        
        return precedents[:5]  # Limit to top 5
    
    def _extract_case_name(self, text: str) -> str:
        """Extract case name from text"""
        # Look for common case name patterns
        patterns = [
            r'([A-Z][a-zA-Z\s&]+)\s+v\.?\s+([A-Z][a-zA-Z\s&]+)',
            r'([A-Z][a-zA-Z\s&]+)\s+vs\.?\s+([A-Z][a-zA-Z\s&]+)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                return f"{match.group(1)} v. {match.group(2)}"
        
        return ""
    
    def _extract_court(self, text: str) -> str:
        """Extract court name from text"""
        if "Supreme Court" in text:
            return "Supreme Court of India"
        elif "High Court" in text:
            # Try to find specific high court
            for state in ["Delhi", "Bombay", "Madras", "Calcutta", "Karnataka", "Punjab"]:
                if f"{state} High Court" in text:
                    return f"{state} High Court"
            return "High Court"
        return "Unknown"
    
    def _extract_year(self, text: str) -> str:
        """Extract year from text"""
        year_match = re.search(r'\b(19|20)\d{2}\b', text)
        return year_match.group(0) if year_match else ""
    
    def _extract_citation(self, text: str) -> str:
        """Extract legal citation from text"""
        # Look for common citation patterns
        patterns = [
            r'\(\d{4}\)\s+\d+\s+SCC\s+\d+',
            r'AIR\s+\d{4}\s+SC\s+\d+',
            r'\d{4}\s+\(\d+\)\s+SCC\s+\d+'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(0)
        
        return ""
    
    def _extract_principle(self, text: str) -> str:
        """Extract legal principle from text"""
        # Look for principle indicators
        principle_indicators = ["held", "established", "principle", "law", "rule"]
        
        sentences = text.split('. ')
        for sentence in sentences:
            if any(indicator in sentence.lower() for indicator in principle_indicators):
                return sentence.strip()
        
        return ""
    
    def _extract_relevance(self, text: str) -> str:
        """Extract relevance explanation from text"""
        # Look for relevance indicators
        relevance_indicators = ["relevant", "applies", "similar", "applicable"]
        
        sentences = text.split('. ')
        for sentence in sentences:
            if any(indicator in sentence.lower() for indicator in relevance_indicators):
                return sentence.strip()
        
        return ""
    
    def _calculate_relevance_scores(self, precedents: List[Dict[str, Any]], query: str) -> List[float]:
        """Calculate relevance scores for precedents"""
        scores = []
        query_words = set(query.lower().split())
        
        for precedent in precedents:
            # Simple scoring based on word overlap
            precedent_text = (precedent.get("summary", "") + " " + 
                            precedent.get("legal_principle", "") + " " + 
                            precedent.get("case_name", "")).lower()
            
            precedent_words = set(precedent_text.split())
            overlap = len(query_words.intersection(precedent_words))
            score = min(overlap / len(query_words), 1.0) if query_words else 0.5
            
            # Boost score for Supreme Court cases
            if "Supreme Court" in precedent.get("court", ""):
                score = min(score + 0.2, 1.0)
            
            scores.append(round(score, 2))
        
        return scores
    
    def _extract_citations(self, precedents: List[Dict[str, Any]]) -> List[str]:
        """Extract formatted citations from precedents"""
        citations = []
        
        for precedent in precedents:
            citation_parts = []
            
            if precedent.get("case_name"):
                citation_parts.append(precedent["case_name"])
            
            if precedent.get("citation"):
                citation_parts.append(precedent["citation"])
            elif precedent.get("year") and precedent.get("court"):
                citation_parts.append(f"{precedent['year']} {precedent['court']}")
            
            if citation_parts:
                citations.append(", ".join(citation_parts))
            else:
                citations.append("Citation not available")
        
        return citations
# update Sun Jul  6 02:54:59 IST 2025
# update Sun Jul  6 02:56:34 IST 2025
