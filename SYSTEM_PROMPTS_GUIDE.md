# LegalDoc System Prompts Implementation Guide

This guide explains how the comprehensive system prompts have been implemented in the LegalDoc application to provide better, more accurate legal assistance focused on Indian law.

## Overview

The system prompts have been integrated across multiple components of the application to ensure consistent, safe, and accurate responses. The implementation follows prompt engineering best practices with a focus on Indian legal standards.

## Implementation Details

### 1. Environment Configuration

**Location:** `backend/.env` and `backend/.env.example`

All system prompts are now configurable through environment variables, allowing for easy customization without code changes.

**Key Environment Variables:**
- `SYSTEM_PROMPT`: Main conversational AI prompt
- `AI_SERVICE_PROMPT`: Context-aware responses with source attribution
- `CLAUSE_EXTRACTION_PROMPT`: Legal clause analysis
- `COMPLIANCE_CHECK_PROMPT`: Regulatory compliance checking
- `PRECEDENT_SEARCH_PROMPT`: Legal precedent search
- `NO_DOCUMENTS_PROMPT`: Special case handling

### 2. Updated Components

#### A. LLM Client (`backend/llm/client.py`)
- **Primary System Prompt**: Implements safety guidelines and Indian law focus
- **Context Limits**: Configurable truncation based on environment settings
- **Response Limits**: Prevents excessively long responses (800 chars max)
- **Timeout Configuration**: Configurable request timeouts (30 seconds default)
- **Smart Prompt Handling**: Different prompts for document analysis vs. general queries

**Key Features:**
- No hallucination policy
- Conservative responses with "I don't know" when uncertain
- Scope limitation to legal document analysis
- Professional yet approachable tone

#### B. AI Service (`backend/app/services/ai_service.py`)
- **Context-Aware Responses**: Enhanced responses based on available context
- **Source Attribution**: Automatic citation extraction and source linking
- **Confidence Scoring**: Algorithmic confidence assessment
- **Legal Analysis Tools**: Specialized methods for contract analysis, compliance checking

**New Classes:**
- `AIService`: Core AI functionality with enhanced context handling
- `LegalAnalysisService`: Specialized legal document analysis tools

#### C. Legal Analysis Service (`backend/app/services/legal_analysis.py`)
- **Environment-Based Prompts**: All prompts now load from environment variables
- **Comprehensive Clause Analysis**: 9 types of legal clauses analyzed
- **Indian Law Compliance**: Focus on Indian Contract Act, Companies Act, SEBI, etc.
- **Precedent Search**: Structured search for relevant Indian case law

### 3. Prompt Engineering Principles

#### Safety & Accuracy
- **No Hallucination**: Strict requirement to only use provided context
- **Conservative Responses**: "I don't know" when uncertain
- **Source Attribution**: Always cite sources when available
- **Scope Limitation**: Stay within legal document analysis domain

#### Indian Legal Focus
- **Jurisdiction Specific**: All analysis focused on Indian law
- **Comprehensive Coverage**: Multiple legal areas covered
- **Court Hierarchy**: Recognition of Supreme Court and High Court precedents
- **Current Regulations**: Updated legal frameworks and recent acts

#### User Experience
- **Professional Tone**: Formal yet approachable
- **Structured Output**: Clear sections and formatting
- **Risk Assessment**: Explicit risk levels and explanations
- **Actionable Recommendations**: Specific improvement suggestions

### 4. Configuration Parameters

The following parameters can be configured via environment variables:

```bash
# Response Control
MAX_OUTPUT_TOKENS=500          # Maximum tokens in AI response
TEMPERATURE=0.7                # AI creativity/randomness level
RESPONSE_LIMIT=800             # Maximum characters in response

# Input Processing  
CONTEXT_TRUNCATION_LIMIT=2500  # Maximum context characters
PROMPT_TRUNCATION_LIMIT=800    # Maximum prompt characters

# Performance
REQUEST_TIMEOUT=30             # API request timeout in seconds
```

## Usage Examples

### 1. General Legal Query
```python
from app.services.ai_service import ai_service

response = ai_service.generate_response(
    user_query="What are the requirements for a valid contract in India?",
    context="",  # No specific document context
    document_type=None
)
```

### 2. Document Analysis
```python
response = ai_service.generate_response(
    user_query="Analyze the termination clauses in this contract",
    context=document_content,
    document_type="Employment Contract"
)
```

### 3. Clause Extraction
```python
from app.services.legal_analysis import ClauseExtractor

extractor = ClauseExtractor()
result = extractor.extract_clauses(document_content)
```

### 4. Compliance Check
```python
from app.services.legal_analysis import ComplianceChecker

checker = ComplianceChecker()
result = checker.check_compliance(document_content, jurisdiction="india")
```

## Safety Features

### 1. Hallucination Prevention
- Context dependency: Only responds based on provided documents
- Uncertainty handling: Clear "I don't know" responses
- Source requirements: Must cite sources for legal claims

### 2. Scope Limitation
- Domain focus: Legal document analysis only
- Polite declining: Graceful handling of out-of-scope queries
- Professional boundaries: Maintains legal assistant role

### 3. Response Quality Control
- Length limits: Prevents overwhelming responses
- Confidence scoring: Algorithmic assessment of response quality
- Error handling: Graceful degradation on failures

## Customization Guide

### 1. Modifying System Prompts

To customize prompts, update the corresponding environment variable in `.env`:

```bash
# Example: Modify the main system prompt
SYSTEM_PROMPT="Your custom prompt here..."
```

### 2. Adding New Legal Areas

To add new legal analysis areas:

1. Update `CLAUSE_TYPES` in `ClauseExtractor`
2. Add new regulation in `INDIAN_REGULATIONS` in `ComplianceChecker`
3. Update the comprehensive analysis prompts

### 3. Adjusting Response Behavior

Modify these parameters to change AI behavior:

```bash
TEMPERATURE=0.5      # More conservative responses
MAX_OUTPUT_TOKENS=300  # Shorter responses
RESPONSE_LIMIT=600   # Stricter length control
```

## Testing and Validation

### 1. Response Quality Testing
- Test with various document types
- Verify Indian law focus
- Check source attribution accuracy
- Validate confidence scoring

### 2. Safety Testing
- Test with out-of-scope queries
- Verify hallucination prevention
- Check uncertainty handling
- Test error scenarios

### 3. Performance Testing
- Response time validation
- Memory usage monitoring
- Timeout handling
- Load testing

## Best Practices

### 1. Environment Management
- Always use `.env.example` as template
- Keep production and development configs separate
- Regularly review and update prompts
- Document any prompt modifications

### 2. Monitoring
- Monitor response quality metrics
- Track confidence scores
- Log unusual patterns
- Regular legal accuracy reviews

### 3. Updates
- Stay current with Indian legal changes
- Update prompts for new regulations
- Regular prompt effectiveness reviews
- User feedback integration

## Troubleshooting

### Common Issues

1. **Empty Responses**: Check API key and network connectivity
2. **Long Response Times**: Adjust timeout settings
3. **Irrelevant Responses**: Review context quality and prompt specificity
4. **Low Confidence Scores**: Improve document quality and context relevance

### Debug Settings

Enable debug mode for detailed logging:

```bash
DEBUG=True
LOG_LEVEL=DEBUG
```

## Future Enhancements

### Planned Improvements
1. **Advanced Legal Reasoning**: More sophisticated legal analysis
2. **Multi-Language Support**: Hindi and other Indian languages
3. **Real-Time Legal Updates**: Integration with legal databases
4. **Enhanced Citation**: Automatic case law verification
5. **User Customization**: User-specific prompt preferences

---

This implementation provides a robust foundation for legal AI assistance while maintaining strict safety and accuracy standards. The modular design allows for easy customization and future enhancements while ensuring consistent, high-quality responses focused on Indian legal standards.
