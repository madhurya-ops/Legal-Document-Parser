import { Document, Analysis, AnalysisType, ClauseExtractionResult, ComplianceCheckResult, PrecedentSearchResult } from '../types/document';
import { api } from './api';

export const uploadDocument = async (
  file: File,
  onProgress?: (progress: number) => void
): Promise<Document> => {
  const formData = new FormData();
  formData.append('file', file);

  const response = await api.post('/documents/upload', formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    },
    onUploadProgress: (progressEvent) => {
      if (onProgress && progressEvent.total) {
        const progress = Math.round((progressEvent.loaded * 100) / progressEvent.total);
        onProgress(progress);
      }
    }
  });

  return response.data.document;
};

export const getDocuments = async (
  page = 1,
  limit = 20,
  search?: string
): Promise<Document[]> => {
  const params = new URLSearchParams({
    page: page.toString(),
    limit: limit.toString()
  });
  
  if (search) {
    params.append('search', search);
  }

  const response = await api.get(`/documents?${params.toString()}`);
  return response.data;
};

export const getDocument = async (documentId: string): Promise<Document> => {
  const response = await api.get(`/documents/${documentId}`);
  return response.data;
};

export const deleteDocument = async (documentId: string): Promise<void> => {
  await api.delete(`/documents/${documentId}`);
};

export const analyzeDocument = async (
  documentId: string,
  analysisType: AnalysisType
): Promise<Analysis> => {
  const response = await api.post(`/documents/${documentId}/analyze`, {
    analysis_type: analysisType
  });
  return response.data;
};

export const searchDocuments = async (query: string): Promise<Document[]> => {
  const response = await api.get('/documents/search', {
    params: { q: query }
  });
  return response.data;
};

// Legal Analysis Functions
export const extractClauses = async (
  documentId: string
): Promise<ClauseExtractionResult> => {
  const response = await api.post('/legal/extract-clauses', {
    document_id: documentId
  });
  return response.data;
};

export const checkCompliance = async (
  documentId: string,
  jurisdiction = 'india'
): Promise<ComplianceCheckResult> => {
  const response = await api.post('/legal/compliance-check', {
    document_id: documentId,
    jurisdiction
  });
  return response.data;
};

export const searchPrecedents = async (
  query: string,
  jurisdiction = 'india',
  documentType?: string
): Promise<PrecedentSearchResult> => {
  const response = await api.post('/legal/precedent-search', {
    query,
    jurisdiction,
    document_type: documentType
  });
  return response.data;
};

export const assessRisk = async (documentId: string): Promise<any> => {
  const response = await api.post('/legal/risk-assessment', {
    document_id: documentId
  });
  return response.data;
};

export const getDocumentPreview = async (documentId: string): Promise<string> => {
  const response = await api.get(`/documents/${documentId}/preview`);
  return response.data.preview_url;
};

export const downloadDocument = async (documentId: string): Promise<void> => {
  const response = await api.get(`/documents/${documentId}/download`, {
    responseType: 'blob'
  });

  // Create download link
  const blob = new Blob([response.data]);
  const url = window.URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = url;
  
  // Get filename from response headers
  const contentDisposition = response.headers['content-disposition'];
  const filename = contentDisposition
    ? contentDisposition.split('filename=')[1]?.replace(/"/g, '')
    : `document-${documentId}`;
    
  link.download = filename;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  window.URL.revokeObjectURL(url);
};

export const shareDocument = async (
  documentId: string,
  permissions: string[],
  expiresAt?: Date
): Promise<{ shareUrl: string }> => {
  const response = await api.post(`/documents/${documentId}/share`, {
    permissions,
    expires_at: expiresAt?.toISOString()
  });
  return response.data;
};

export const getSharedDocument = async (shareToken: string): Promise<Document> => {
  const response = await api.get(`/documents/shared/${shareToken}`);
  return response.data;
};
