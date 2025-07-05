export interface Document {
  id: string;
  filename: string;
  originalFilename: string;
  fileHash: string;
  fileSize: string;
  fileType: string;
  userId: string;
  createdAt: Date;
  updatedAt?: Date;
  analysisHistory?: Analysis[];
  metadata?: DocumentMetadata;
  textContent?: string;
  thumbnail?: string;
}

export interface DocumentMetadata {
  author?: string;
  title?: string;
  subject?: string;
  creator?: string;
  producer?: string;
  creationDate?: Date;
  modificationDate?: Date;
  pageCount?: number;
  wordCount?: number;
  language?: string;
  documentType?: DocumentType;
}

export enum DocumentType {
  CONTRACT = 'contract',
  AGREEMENT = 'agreement',
  LEGAL_BRIEF = 'legal_brief',
  COURT_FILING = 'court_filing',
  MEMORANDUM = 'memorandum',
  POLICY = 'policy',
  REGULATION = 'regulation',
  OTHER = 'other'
}

export enum AnalysisType {
  CLAUSE_EXTRACTION = 'clause_extraction',
  DOCUMENT_SUMMARY = 'document_summary',
  COMPLIANCE_CHECK = 'compliance_check',
  PRECEDENT_SEARCH = 'precedent_search',
  RISK_ASSESSMENT = 'risk_assessment'
}

export interface Analysis {
  id: string;
  documentId: string;
  analysisType: AnalysisType;
  results: Record<string, any>;
  confidence?: number;
  createdAt: Date;
  processingTime?: number;
  status: AnalysisStatus;
}

export enum AnalysisStatus {
  PENDING = 'pending',
  PROCESSING = 'processing',
  COMPLETED = 'completed',
  FAILED = 'failed'
}

export interface ClauseExtractionResult {
  clauses: Clause[];
  confidenceScores: Record<string, number>;
  riskAssessment: RiskAssessment;
  recommendations: string[];
}

export interface Clause {
  id: string;
  type: ClauseType;
  content: string;
  location: ClauseLocation;
  importance: ImportanceLevel;
  riskLevel: RiskLevel;
  suggestions?: string[];
}

export enum ClauseType {
  PAYMENT = 'payment',
  TERMINATION = 'termination',
  LIABILITY = 'liability',
  INTELLECTUAL_PROPERTY = 'intellectual_property',
  CONFIDENTIALITY = 'confidentiality',
  DISPUTE_RESOLUTION = 'dispute_resolution',
  FORCE_MAJEURE = 'force_majeure',
  GOVERNING_LAW = 'governing_law',
  WARRANTIES = 'warranties',
  INDEMNIFICATION = 'indemnification',
  OTHER = 'other'
}

export interface ClauseLocation {
  page?: number;
  section?: string;
  paragraph?: number;
  startPosition?: number;
  endPosition?: number;
}

export enum ImportanceLevel {
  LOW = 'low',
  MEDIUM = 'medium',
  HIGH = 'high',
  CRITICAL = 'critical'
}

export enum RiskLevel {
  LOW = 'low',
  MEDIUM = 'medium',
  HIGH = 'high',
  CRITICAL = 'critical'
}

export interface RiskAssessment {
  overallRisk: RiskLevel;
  riskFactors: RiskFactor[];
  mitigationSuggestions: string[];
  complianceScore: number;
}

export interface RiskFactor {
  type: string;
  description: string;
  severity: RiskLevel;
  likelihood: number;
  impact: number;
}

export interface DocumentUploadProps {
  onUpload: (files: File[]) => void;
  acceptedTypes?: string[];
  maxSize?: number;
  multiple?: boolean;
}

export interface DocumentViewerProps {
  document: Document;
  annotations?: Annotation[];
  onAnnotate?: (annotation: Annotation) => void;
}

export interface Annotation {
  id: string;
  documentId: string;
  userId: string;
  type: AnnotationType;
  content: string;
  location: ClauseLocation;
  createdAt: Date;
  updatedAt?: Date;
}

export enum AnnotationType {
  HIGHLIGHT = 'highlight',
  COMMENT = 'comment',
  SUGGESTION = 'suggestion',
  WARNING = 'warning'
}

export interface DocumentListProps {
  documents: Document[];
  onDocumentSelect: (document: Document) => void;
  onDocumentDelete: (documentId: string) => void;
  searchQuery?: string;
  sortBy?: DocumentSortField;
  sortOrder?: 'asc' | 'desc';
}

export enum DocumentSortField {
  NAME = 'name',
  DATE = 'date',
  SIZE = 'size',
  TYPE = 'type'
}

export interface ComplianceCheckResult {
  status: ComplianceStatus;
  missingClauses: string[];
  regulatoryRequirements: RegulatoryRequirement[];
  recommendations: string[];
  confidenceScore: number;
}

export enum ComplianceStatus {
  COMPLIANT = 'compliant',
  PARTIALLY_COMPLIANT = 'partially_compliant',
  NON_COMPLIANT = 'non_compliant',
  UNKNOWN = 'unknown'
}

export interface RegulatoryRequirement {
  id: string;
  title: string;
  description: string;
  jurisdiction: string;
  severity: ImportanceLevel;
  compliance: boolean;
}

export interface PrecedentSearchResult {
  precedents: LegalPrecedent[];
  relevanceScores: number[];
  citations: string[];
}

export interface LegalPrecedent {
  id: string;
  title: string;
  court: string;
  date: Date;
  citation: string;
  summary: string;
  relevance: number;
  url?: string;
}

