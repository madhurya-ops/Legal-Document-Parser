export enum MessageType {
  USER = 'user',
  ASSISTANT = 'assistant',
  SYSTEM = 'system'
}

export interface Source {
  id: string;
  title: string;
  content: string;
  url?: string;
  relevance: number;
}

export interface Message {
  id: string;
  type: MessageType;
  content: string;
  timestamp: Date;
  sources?: Source[];
  confidence?: number;
  metadata?: Record<string, any>;
  sessionId?: string;
}

export interface ChatSession {
  id: string;
  userId: string;
  name?: string;
  createdAt: Date;
  updatedAt?: Date;
  messages: Message[];
  documentIds?: string[];
}

export interface ChatResponse {
  success: boolean;
  message?: string;
  sources?: Source[];
  confidence?: number;
  suggestedQuestions?: string[];
  error?: string;
}

export interface StreamChunk {
  type: 'chunk' | 'end' | 'error';
  content?: string;
  metadata?: Record<string, any>;
}

export interface ChatInterfaceProps {
  sessionId?: string;
  documents?: Document[];
  onDocumentUpload?: (file: File) => void;
}

export interface MessageInputProps {
  onSend: (message: string, files?: File[]) => void;
  disabled?: boolean;
  placeholder?: string;
  maxLength?: number;
}

export interface MessageListProps {
  messages: Message[];
  isLoading?: boolean;
}

export interface ChatHistoryProps {
  sessions: ChatSession[];
  activeSession?: ChatSession;
  onSessionSelect: (sessionId: string) => void;
  onSessionDelete: (sessionId: string) => void;
}

export enum ExportFormat {
  PDF = 'pdf',
  DOCX = 'docx',
  TXT = 'txt',
  HTML = 'html'
}
