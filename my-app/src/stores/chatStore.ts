import { create } from 'zustand';
import { ChatSession, Message, ChatResponse, ExportFormat, MessageType } from '../types/chat';
import * as chatService from '../services/chat';

interface ChatStore {
  sessions: ChatSession[];
  activeSession: ChatSession | null;
  messages: Message[];
  isLoading: boolean;
  isConnected: boolean;
  
  // Actions
  createSession: (name?: string) => Promise<ChatSession>;
  selectSession: (sessionId: string) => void;
  sendMessage: (content: string, files?: File[]) => Promise<void>;
  deleteSession: (sessionId: string) => Promise<void>;
  exportSession: (sessionId: string, format: ExportFormat) => Promise<void>;
  loadSessions: () => Promise<void>;
  loadMessages: (sessionId: string) => Promise<void>;
  addMessage: (message: Message) => void;
  setLoading: (loading: boolean) => void;
  setConnected: (connected: boolean) => void;
  clearMessages: () => void;
}

export const useChatStore = create<ChatStore>((set, get) => ({
  sessions: [],
  activeSession: null,
  messages: [],
  isLoading: false,
  isConnected: false,

  createSession: async (name?: string) => {
    try {
      set({ isLoading: true });
      const session = await chatService.createSession(name);
      
      set(state => ({
        sessions: [session, ...state.sessions],
        activeSession: session,
        messages: [],
        isLoading: false
      }));
      
      return session;
    } catch (error) {
      set({ isLoading: false });
      throw error;
    }
  },

  selectSession: (sessionId: string) => {
    const { sessions } = get();
    const session = sessions.find(s => s.id === sessionId);
    
    if (session) {
      set({
        activeSession: session,
        messages: session.messages || []
      });
    }
  },

  sendMessage: async (content: string, files?: File[]) => {
    const { activeSession } = get();
    if (!activeSession) {
      throw new Error('No active session');
    }

    try {
      set({ isLoading: true });
      
      // Add user message immediately
      const userMessage: Message = {
        id: crypto.randomUUID(),
        type: MessageType.USER,
        content,
        timestamp: new Date(),
        sessionId: activeSession.id
      };
      
      get().addMessage(userMessage);
      
      // Send to backend
      const response = await chatService.sendMessage(activeSession.id, content, files);
      
      if (response.success && response.message) {
        // Add assistant response
        const assistantMessage: Message = {
          id: crypto.randomUUID(),
          type: MessageType.ASSISTANT,
          content: response.message,
          timestamp: new Date(),
          sessionId: activeSession.id,
          sources: response.sources,
          confidence: response.confidence
        };
        
        get().addMessage(assistantMessage);
      }
      
      set({ isLoading: false });
    } catch (error) {
      set({ isLoading: false });
      throw error;
    }
  },

  deleteSession: async (sessionId: string) => {
    try {
      await chatService.deleteSession(sessionId);
      
      set(state => {
        const newSessions = state.sessions.filter(s => s.id !== sessionId);
        const newActiveSession = state.activeSession?.id === sessionId 
          ? (newSessions[0] || null) 
          : state.activeSession;
        
        return {
          sessions: newSessions,
          activeSession: newActiveSession,
          messages: newActiveSession?.messages || []
        };
      });
    } catch (error) {
      throw error;
    }
  },

  exportSession: async (sessionId: string, format: ExportFormat) => {
    try {
      await chatService.exportSession(sessionId, format);
    } catch (error) {
      throw error;
    }
  },

  loadSessions: async () => {
    try {
      set({ isLoading: true });
      const sessions = await chatService.getSessions();
      
      set({
        sessions,
        isLoading: false
      });
    } catch (error) {
      set({ isLoading: false });
      throw error;
    }
  },

  loadMessages: async (sessionId: string) => {
    try {
      set({ isLoading: true });
      const messages = await chatService.getMessages(sessionId);
      
      set({
        messages,
        isLoading: false
      });
    } catch (error) {
      set({ isLoading: false });
      throw error;
    }
  },

  addMessage: (message: Message) => {
    set(state => ({
      messages: [...state.messages, message]
    }));
  },

  setLoading: (loading: boolean) => {
    set({ isLoading: loading });
  },

  setConnected: (connected: boolean) => {
    set({ isConnected: connected });
  },

  clearMessages: () => {
    set({ messages: [] });
  }
}));

