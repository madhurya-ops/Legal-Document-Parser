import { ChatSession, Message, ChatResponse, ExportFormat } from '../types/chat';
import { api } from './api';

export const createSession = async (name?: string): Promise<ChatSession> => {
  const response = await api.post('/chat/sessions', { session_name: name });
  return response.data;
};

export const getSessions = async (): Promise<ChatSession[]> => {
  const response = await api.get('/chat/sessions');
  return response.data;
};

export const getSession = async (sessionId: string): Promise<ChatSession> => {
  const response = await api.get(`/chat/sessions/${sessionId}`);
  return response.data;
};

export const deleteSession = async (sessionId: string): Promise<void> => {
  await api.delete(`/chat/sessions/${sessionId}`);
};

export const sendMessage = async (
  sessionId: string, 
  content: string, 
  files?: File[]
): Promise<ChatResponse> => {
  const formData = new FormData();
  formData.append('session_id', sessionId);
  formData.append('message', content);
  
  if (files) {
    files.forEach((file, index) => {
      formData.append(`file_${index}`, file);
    });
  }

  const response = await api.post('/chat/messages', formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  });
  
  return response.data;
};

export const getMessages = async (sessionId: string): Promise<Message[]> => {
  const response = await api.get(`/chat/sessions/${sessionId}/messages`);
  return response.data;
};

export const streamMessage = async (
  sessionId: string,
  content: string,
  onChunk: (chunk: string) => void,
  onComplete: () => void,
  onError: (error: Error) => void
): Promise<void> => {
  try {
    const response = await fetch(`${api.defaults.baseURL}/chat/stream`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('auth_token')}`
      },
      body: JSON.stringify({
        session_id: sessionId,
        message: content,
        stream: true
      })
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const reader = response.body?.getReader();
    if (!reader) {
      throw new Error('No response body');
    }

    const decoder = new TextDecoder();
    let buffer = '';

    while (true) {
      const { done, value } = await reader.read();
      
      if (done) {
        onComplete();
        break;
      }

      buffer += decoder.decode(value, { stream: true });
      const lines = buffer.split('\n');
      buffer = lines.pop() || '';

      for (const line of lines) {
        if (line.startsWith('data: ')) {
          const data = line.slice(6);
          if (data === '[DONE]') {
            onComplete();
            return;
          }
          
          try {
            const parsed = JSON.parse(data);
            if (parsed.type === 'chunk') {
              onChunk(parsed.content);
            } else if (parsed.type === 'error') {
              onError(new Error(parsed.content));
              return;
            }
          } catch (e) {
            // Ignore parsing errors for malformed chunks
          }
        }
      }
    }
  } catch (error) {
    onError(error instanceof Error ? error : new Error('Unknown error'));
  }
};

export const exportSession = async (
  sessionId: string, 
  format: ExportFormat
): Promise<void> => {
  const response = await api.post(`/chat/sessions/${sessionId}/export`, { format }, {
    responseType: 'blob'
  });
  
  // Create download link
  const blob = new Blob([response.data]);
  const url = window.URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = url;
  link.download = `chat-session-${sessionId}.${format}`;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  window.URL.revokeObjectURL(url);
};

export const updateSessionName = async (
  sessionId: string, 
  name: string
): Promise<ChatSession> => {
  const response = await api.put(`/chat/sessions/${sessionId}`, { session_name: name });
  return response.data;
};

export interface ChatQuery {
  question: string;
  file_content?: string;
}

export interface AskResponse {
  answer: string;
}

export const sendQuery = async (payload: ChatQuery): Promise<string> => {
  try {
    const response = await api.post<AskResponse>('/api/ask', payload);
    return response.data.answer;
  } catch (error) {
    console.error('❌ Error querying backend:', error);
    throw new Error('Something went wrong while connecting to the server.');
  }
};

