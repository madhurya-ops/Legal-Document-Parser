import { create } from 'zustand';
import { Document, Analysis, AnalysisType } from '../types/document';
import * as documentService from '../services/document';

interface DocumentStore {
  documents: Document[];
  selectedDocument: Document | null;
  isUploading: boolean;
  uploadProgress: number;
  isLoading: boolean;
  
  // Actions
  uploadDocument: (file: File) => Promise<Document>;
  deleteDocument: (id: string) => Promise<void>;
  selectDocument: (id: string) => void;
  analyzeDocument: (id: string, type: AnalysisType) => Promise<Analysis>;
  searchDocuments: (query: string) => Promise<Document[]>;
  loadDocuments: () => Promise<void>;
  setUploadProgress: (progress: number) => void;
  setLoading: (loading: boolean) => void;
  clearSelection: () => void;
}

export const useDocumentStore = create<DocumentStore>((set, get) => ({
  documents: [],
  selectedDocument: null,
  isUploading: false,
  uploadProgress: 0,
  isLoading: false,

  uploadDocument: async (file: File) => {
    try {
      set({ isUploading: true, uploadProgress: 0 });
      
      const document = await documentService.uploadDocument(file, (progress) => {
        set({ uploadProgress: progress });
      });
      
      set(state => ({
        documents: [document, ...state.documents],
        selectedDocument: document,
        isUploading: false,
        uploadProgress: 100
      }));
      
      return document;
    } catch (error) {
      set({ isUploading: false, uploadProgress: 0 });
      throw error;
    }
  },

  deleteDocument: async (id: string) => {
    try {
      await documentService.deleteDocument(id);
      
      set(state => ({
        documents: state.documents.filter(doc => doc.id !== id),
        selectedDocument: state.selectedDocument?.id === id ? null : state.selectedDocument
      }));
    } catch (error) {
      throw error;
    }
  },

  selectDocument: (id: string) => {
    const { documents } = get();
    const document = documents.find(doc => doc.id === id);
    
    if (document) {
      set({ selectedDocument: document });
    }
  },

  analyzeDocument: async (id: string, type: AnalysisType) => {
    try {
      set({ isLoading: true });
      const analysis = await documentService.analyzeDocument(id, type);
      
      // Update document with new analysis
      set(state => ({
        documents: state.documents.map(doc => 
          doc.id === id 
            ? { ...doc, analysisHistory: [...(doc.analysisHistory || []), analysis] }
            : doc
        ),
        isLoading: false
      }));
      
      return analysis;
    } catch (error) {
      set({ isLoading: false });
      throw error;
    }
  },

  searchDocuments: async (query: string) => {
    try {
      set({ isLoading: true });
      const results = await documentService.searchDocuments(query);
      
      set({ isLoading: false });
      return results;
    } catch (error) {
      set({ isLoading: false });
      throw error;
    }
  },

  loadDocuments: async () => {
    try {
      set({ isLoading: true });
      const documents = await documentService.getDocuments();
      
      set({
        documents,
        isLoading: false
      });
    } catch (error) {
      set({ isLoading: false });
      throw error;
    }
  },

  setUploadProgress: (progress: number) => {
    set({ uploadProgress: progress });
  },

  setLoading: (loading: boolean) => {
    set({ isLoading: loading });
  },

  clearSelection: () => {
    set({ selectedDocument: null });
  }
}));
