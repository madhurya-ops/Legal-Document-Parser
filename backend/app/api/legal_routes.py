from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
import logging

from .. import crud, schemas, auth
from ..database import get_db
from ..services.legal_analysis import ClauseExtractor, ComplianceChecker, PrecedentEngine

router = APIRouter(prefix="/legal", tags=["legal"])
logger = logging.getLogger(__name__)

# Initialize services
clause_extractor = ClauseExtractor()
compliance_checker = ComplianceChecker()
precedent_engine = PrecedentEngine()

@router.post("/extract-clauses", response_model=schemas.ClauseExtractionResponse)
async def extract_legal_clauses(
    request: schemas.ClauseExtractionRequest,
    current_user: schemas.UserResponse = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    """Extract and analyze legal clauses from document content"""
    try:
        # Extract clauses using the service
        result = clause_extractor.extract_clauses(
            document_content=request.document_content,
            document_id=str(request.document_id) if request.document_id else None
        )
        
        # If document_id is provided, save the analysis
        if request.document_id:
            # Verify user owns the document
            document = db.query(crud.models.Document).filter(
                crud.models.Document.id == request.document_id,
                crud.models.Document.user_id == current_user.id
            ).first()
            
            if document:
                # Save analysis to database
                analysis_data = schemas.DocumentAnalysisCreate(
                    document_id=request.document_id,
                    analysis_type=schemas.AnalysisType.CLAUSE_EXTRACTION,
                    results={
                        "clauses": result.clauses,
                        "confidence_scores": result.confidence_scores,
                        "risk_assessment": result.risk_assessment,
                        "recommendations": result.recommendations
                    },
                    confidence_score=sum(result.confidence_scores.values()) / len(result.confidence_scores) if result.confidence_scores else 0.0
                )
                crud.create_document_analysis(db, analysis_data)
        
        return result
        
    except Exception as e:
        logger.error(f"Error extracting clauses: {e}")
        raise HTTPException(status_code=500, detail="Failed to extract clauses")

@router.post("/compliance-check", response_model=schemas.ComplianceCheckResponse)
async def check_compliance(
    request: schemas.ComplianceCheckRequest,
    current_user: schemas.UserResponse = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    """Check document compliance with relevant regulations"""
    try:
        # Check compliance using the service
        result = compliance_checker.check_compliance(
            document_content=request.document_content,
            jurisdiction=request.jurisdiction,
            document_id=str(request.document_id) if request.document_id else None
        )
        
        # If document_id is provided, save the analysis
        if request.document_id:
            # Verify user owns the document
            document = db.query(crud.models.Document).filter(
                crud.models.Document.id == request.document_id,
                crud.models.Document.user_id == current_user.id
            ).first()
            
            if document:
                # Save analysis to database
                analysis_data = schemas.DocumentAnalysisCreate(
                    document_id=request.document_id,
                    analysis_type=schemas.AnalysisType.COMPLIANCE_CHECK,
                    results={
                        "compliance_status": result.compliance_status,
                        "missing_clauses": result.missing_clauses,
                        "regulatory_requirements": result.regulatory_requirements,
                        "recommendations": result.recommendations,
                        "jurisdiction": request.jurisdiction
                    },
                    confidence_score=result.confidence_score
                )
                crud.create_document_analysis(db, analysis_data)
        
        return result
        
    except Exception as e:
        logger.error(f"Error checking compliance: {e}")
        raise HTTPException(status_code=500, detail="Failed to check compliance")

@router.post("/precedent-search", response_model=schemas.PrecedentSearchResponse)
async def search_precedents(
    request: schemas.PrecedentSearchRequest,
    current_user: schemas.UserResponse = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    """Search for relevant legal precedents"""
    try:
        # Search precedents using the service
        result = precedent_engine.find_relevant_precedents(
            query=request.query,
            jurisdiction=request.jurisdiction,
            document_type=request.document_type
        )
        
        return result
        
    except Exception as e:
        logger.error(f"Error searching precedents: {e}")
        raise HTTPException(status_code=500, detail="Failed to search precedents")

@router.get("/documents/{document_id}/analyses", response_model=list[schemas.DocumentAnalysisResponse])
async def get_document_analyses(
    document_id: str,
    current_user: schemas.UserResponse = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get all analyses for a specific document"""
    try:
        analyses = crud.get_document_analyses(db, document_id, str(current_user.id))
        return [schemas.DocumentAnalysisResponse.from_orm(analysis) for analysis in analyses]
        
    except Exception as e:
        logger.error(f"Error fetching document analyses: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch document analyses")

@router.get("/documents/{document_id}/analyses/{analysis_type}", response_model=schemas.DocumentAnalysisResponse)
async def get_document_analysis_by_type(
    document_id: str,
    analysis_type: schemas.AnalysisType,
    current_user: schemas.UserResponse = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get the latest analysis of a specific type for a document"""
    try:
        analysis = crud.get_analysis_by_type(db, document_id, analysis_type.value, str(current_user.id))
        if not analysis:
            raise HTTPException(status_code=404, detail="Analysis not found")
        
        return schemas.DocumentAnalysisResponse.from_orm(analysis)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching document analysis: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch document analysis")

@router.post("/documents/{document_id}/analyze")
async def analyze_document(
    document_id: str,
    analysis_type: schemas.AnalysisType,
    current_user: schemas.UserResponse = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    """Perform specific analysis on a document"""
    try:
        # Verify user owns the document
        document = db.query(crud.models.Document).filter(
            crud.models.Document.id == document_id,
            crud.models.Document.user_id == current_user.id
        ).first()
        
        if not document:
            raise HTTPException(status_code=404, detail="Document not found")
        
        # Read document content (this would need to be implemented)
        # For now, return a placeholder response
        return {
            "message": f"Document analysis for {analysis_type.value} initiated",
            "document_id": document_id,
            "analysis_type": analysis_type.value,
            "status": "pending"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error analyzing document: {e}")
        raise HTTPException(status_code=500, detail="Failed to analyze document")

@router.get("/documents/{document_id}/download")
async def download_analysis(
    document_id: str,
    format: str = "pdf",
    current_user: schemas.UserResponse = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    """Download analysis results in specified format"""
    try:
        # Verify user owns the document
        document = db.query(crud.models.Document).filter(
            crud.models.Document.id == document_id,
            crud.models.Document.user_id == current_user.id
        ).first()
        
        if not document:
            raise HTTPException(status_code=404, detail="Document not found")
        
        # This would generate and return the analysis in the requested format
        # For now, return a placeholder response
        return {
            "message": f"Download analysis in {format} format",
            "document_id": document_id,
            "format": format,
            "download_url": f"/api/legal/documents/{document_id}/download/{format}"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error downloading analysis: {e}")
        raise HTTPException(status_code=500, detail="Failed to download analysis")
# update Sun Jul  6 02:54:59 IST 2025
# update Sun Jul  6 02:56:34 IST 2025
