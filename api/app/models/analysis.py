"""
Analysis Model
==============

Document analysis model for storing AI analysis results.
"""

import enum
import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey, Text, Float, Integer
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from ..core.database import Base


class AnalysisType(enum.Enum):
    """Analysis type enumeration."""
    CLAUSE_EXTRACTION = "clause_extraction"
    DOCUMENT_SUMMARY = "document_summary"
    COMPLIANCE_CHECK = "compliance_check"
    PRECEDENT_SEARCH = "precedent_search"
    RISK_ASSESSMENT = "risk_assessment"
    CONTRACT_REVIEW = "contract_review"
    LEGAL_ENTITY_RECOGNITION = "legal_entity_recognition"


class AnalysisStatus(enum.Enum):
    """Analysis status enumeration."""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class DocumentAnalysis(Base):
    """Document analysis model for storing AI analysis results."""
    
    __tablename__ = "document_analyses"
    
    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Analysis information
    analysis_type = Column(String(50), nullable=False)
    status = Column(String(20), default=AnalysisStatus.PENDING.value)
    
    # Results
    results = Column(JSONB, nullable=True)
    summary = Column(Text, nullable=True)
    
    # Analysis metadata
    confidence_score = Column(Float, nullable=True)
    processing_time = Column(Float, nullable=True)
    model_used = Column(String(100), nullable=True)
    parameters = Column(JSONB, nullable=True)
    
    # Error handling
    error_message = Column(Text, nullable=True)
    retry_count = Column(Integer, default=0)
    
    # Analysis metrics
    tokens_used = Column(Integer, nullable=True)
    cost_estimate = Column(Float, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)
    
    # Foreign keys
    document_id = Column(UUID(as_uuid=True), ForeignKey("documents.id"), nullable=False)
    
    # Relationships
    document = relationship("Document", back_populates="analyses")
    
    def __repr__(self):
        """String representation of analysis."""
        return f"<DocumentAnalysis(id={self.id}, type={self.analysis_type}, status={self.status})>"
    
    @property
    def is_completed(self) -> bool:
        """Check if analysis is completed."""
        return self.status == AnalysisStatus.COMPLETED.value
    
    @property
    def is_failed(self) -> bool:
        """Check if analysis failed."""
        return self.status == AnalysisStatus.FAILED.value
    
    @property
    def is_processing(self) -> bool:
        """Check if analysis is currently processing."""
        return self.status == AnalysisStatus.PROCESSING.value
    
    def mark_completed(self, results: dict = None):
        """Mark analysis as completed."""
        self.status = AnalysisStatus.COMPLETED.value
        self.completed_at = datetime.utcnow()
        if results:
            self.results = results
    
    def mark_failed(self, error_message: str):
        """Mark analysis as failed."""
        self.status = AnalysisStatus.FAILED.value
        self.error_message = error_message
        self.retry_count += 1
    
    def get_result(self, key: str, default=None):
        """Get specific result value."""
        if self.results:
            return self.results.get(key, default)
        return default
    
    def set_result(self, key: str, value):
        """Set specific result value."""
        if self.results is None:
            self.results = {}
        self.results[key] = value
    
    def add_finding(self, category: str, finding: dict):
        """Add a finding to the analysis results."""
        if self.results is None:
            self.results = {}
        
        if "findings" not in self.results:
            self.results["findings"] = {}
        
        if category not in self.results["findings"]:
            self.results["findings"][category] = []
        
        finding["id"] = str(uuid.uuid4())
        finding["added_at"] = datetime.utcnow().isoformat()
        self.results["findings"][category].append(finding)
    
    def get_findings(self, category: str = None):
        """Get findings by category or all findings."""
        if not self.results or "findings" not in self.results:
            return [] if category else {}
        
        if category:
            return self.results["findings"].get(category, [])
        else:
            return self.results["findings"]
    
    def calculate_risk_score(self) -> float:
        """Calculate overall risk score from findings."""
        findings = self.get_findings()
        if not findings:
            return 0.0
        
        risk_scores = []
        for category, category_findings in findings.items():
            for finding in category_findings:
                if "risk_level" in finding:
                    # Convert risk levels to numeric scores
                    risk_map = {"low": 1, "medium": 2, "high": 3, "critical": 4}
                    risk_scores.append(risk_map.get(finding["risk_level"].lower(), 0))
        
        if risk_scores:
            return sum(risk_scores) / len(risk_scores)
        return 0.0
    
    def to_dict(self) -> dict:
        """Convert analysis to dictionary."""
        return {
            "id": str(self.id),
            "analysis_type": self.analysis_type,
            "status": self.status,
            "results": self.results,
            "summary": self.summary,
            "confidence_score": self.confidence_score,
            "processing_time": self.processing_time,
            "model_used": self.model_used,
            "parameters": self.parameters,
            "error_message": self.error_message,
            "retry_count": self.retry_count,
            "tokens_used": self.tokens_used,
            "cost_estimate": self.cost_estimate,
            "risk_score": self.calculate_risk_score(),
            "is_completed": self.is_completed,
            "is_failed": self.is_failed,
            "is_processing": self.is_processing,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "document_id": str(self.document_id)
        }
