// Configuration from environment variables
const API_CONFIG = {
  baseURL: (process.env.REACT_APP_API_URL || 'http://localhost:8000').replace(/\/+$/, ''),
  timeout: parseInt(process.env.REACT_APP_API_TIMEOUT) || 90000,  // Increased timeout for detailed responses (90 seconds)
  retries: parseInt(process.env.REACT_APP_API_RETRIES) || 3,
};

// Enhanced error handling and retry logic
const fetchWithRetry = async (url, options, retries = API_CONFIG.retries) => {
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), API_CONFIG.timeout);
  
  try {
    const response = await fetch(url, {
      ...options,
      signal: controller.signal,
    });
    clearTimeout(timeoutId);
    
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }
    
    return response;
  } catch (error) {
    clearTimeout(timeoutId);
    
    if (retries > 0 && error.name !== 'AbortError') {
      console.warn(`Request failed, retrying... (${retries} attempts left)`);
      await new Promise(resolve => setTimeout(resolve, 1000));
      return fetchWithRetry(url, options, retries - 1);
    }
    
    throw error;
  }
};

// Sends a question to the FastAPI backend and returns the answer
export const sendQuery = async (payload, getAccessTokenSilently = null) => {
  try {
    const headers = {
      'Content-Type': 'application/json',
    };
    
    if (getAccessTokenSilently) {
      try {
        const token = await getAccessTokenSilently({
          audience: 'https://legaldoc-api'
        });
        headers['Authorization'] = `Bearer ${token}`;
      } catch (error) {
        console.warn('Could not get Auth0 token, proceeding without authentication:', error);
      }
    }
    
    const response = await fetchWithRetry(`${API_CONFIG.baseURL}/api/query/ask`, {
      method: 'POST',
      headers,
      body: JSON.stringify(payload),
    });
    
    const data = await response.json();
    
    if (data && typeof data === 'object') {
      if ('answer' in data) {
        return data.answer;
      } else {
        return JSON.stringify(data);
      }
    } else {
      return String(data);
    }
  } catch (error) {
    console.error('❌ Error querying backend:', error);
    
    if (error.name === 'AbortError') {
      return 'Request timed out. Please try again with a shorter question or check your connection.';
    }
    
    return 'Something went wrong while connecting to the server. Please try again.';
  }
};

// Auth API helpers
const baseURL = (process.env.REACT_APP_API_URL || 'http://localhost:8000').replace(/\/+$/, '');

export const loginUser = async (email, password) => {
  const response = await fetch(`${baseURL}/api/auth/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password })
  });
  if (!response.ok) throw new Error((await response.json()).detail || 'Login failed');
  return response.json();
};

export const signupUser = async (username, email, password) => {
  const response = await fetch(`${baseURL}/api/auth/signup`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username, email, password })
  });
  if (!response.ok) throw new Error((await response.json()).detail || 'Signup failed');
  return response.json();
};

export const getCurrentUser = async (token) => {
  const response = await fetch(`${baseURL}/api/auth/me`, {
    method: 'GET',
    headers: { 'Authorization': `Bearer ${token}` }
  });
  if (!response.ok) throw new Error('Invalid token');
  return response.json();
};

export const updateUserProfile = async (userData) => {
  const token = getToken();
  if (!token) throw new Error('Authentication required');
  
  const response = await fetch(`${baseURL}/api/auth/profile`, {
    method: 'PUT',
    headers: { 
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}` 
    },
    body: JSON.stringify(userData)
  });
  if (!response.ok) throw new Error((await response.json()).detail || 'Failed to update profile');
  return response.json();
};

// These functions are now replaced by Auth0's token management
export function storeToken(token) {
  console.warn('storeToken is deprecated and managed by Auth0');
}
export function getToken() {
  console.warn('getToken is deprecated, use Auth0 context for tokens');
  return null;
}
export function clearToken() {
  console.warn('clearToken is deprecated and managed by Auth0');
}

// Admin API helpers
export const getAdminDashboard = async () => {
  const token = getToken();
  if (!token) throw new Error('Authentication required');
  
  const response = await fetch(`${baseURL}/api/admin/dashboard`, {
    method: 'GET',
    headers: { 'Authorization': `Bearer ${token}` }
  });
  if (!response.ok) throw new Error((await response.json()).detail || 'Failed to fetch dashboard');
  return response.json();
};

export const getAllUsers = async (skip = 0, limit = 100) => {
  const token = getToken();
  if (!token) throw new Error('Authentication required');
  
  const response = await fetch(`${baseURL}/api/admin/users?skip=${skip}&limit=${limit}`, {
    method: 'GET',
    headers: { 'Authorization': `Bearer ${token}` }
  });
  if (!response.ok) throw new Error((await response.json()).detail || 'Failed to fetch users');
  return response.json();
};

export const updateUser = async (userId, userUpdate) => {
  const token = getToken();
  if (!token) throw new Error('Authentication required');
  
  const response = await fetch(`${baseURL}/api/admin/users/${userId}`, {
    method: 'PUT',
    headers: { 
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}` 
    },
    body: JSON.stringify(userUpdate)
  });
  if (!response.ok) throw new Error((await response.json()).detail || 'Failed to update user');
  return response.json();
};

export const getSystemMetrics = async (metricName = null, days = 7) => {
  const token = getToken();
  if (!token) throw new Error('Authentication required');
  
  const params = new URLSearchParams({ days: days.toString() });
  if (metricName) params.append('metric_name', metricName);
  
  const response = await fetch(`${baseURL}/api/admin/metrics?${params}`, {
    method: 'GET',
    headers: { 'Authorization': `Bearer ${token}` }
  });
  if (!response.ok) throw new Error((await response.json()).detail || 'Failed to fetch metrics');
  return response.json();
};

export const getVectorCollections = async () => {
  const token = getToken();
  if (!token) throw new Error('Authentication required');
  
  const response = await fetch(`${baseURL}/api/admin/vector-collections`, {
    method: 'GET',
    headers: { 'Authorization': `Bearer ${token}` }
  });
  if (!response.ok) throw new Error((await response.json()).detail || 'Failed to fetch vector collections');
  return response.json();
};

// Document API helpers
export const getAllDocuments = async (skip = 0, limit = 100) => {
  const token = getToken();
  if (!token) throw new Error('Authentication required');
  
  const response = await fetch(`${baseURL}/api/documents?skip=${skip}&limit=${limit}`, {
    method: 'GET',
    headers: { 'Authorization': `Bearer ${token}` }
  });
  if (!response.ok) throw new Error((await response.json()).detail || 'Failed to fetch documents');
  return response.json();
};

export const uploadDocument = async (file) => {
  const token = getToken();
  if (!token) throw new Error('Authentication required');
  
  const formData = new FormData();
  formData.append('file', file);
  
  const response = await fetch(`${baseURL}/api/documents/upload`, {
    method: 'POST',
    headers: { 'Authorization': `Bearer ${token}` },
    body: formData
  });
  if (!response.ok) throw new Error((await response.json()).detail || 'Failed to upload document');
  return response.json();
};

export const deleteDocument = async (documentId) => {
  const token = getToken();
  if (!token) throw new Error('Authentication required');
  
  const response = await fetch(`${baseURL}/api/documents/${documentId}`, {
    method: 'DELETE',
    headers: { 'Authorization': `Bearer ${token}` }
  });
  if (!response.ok) throw new Error((await response.json()).detail || 'Failed to delete document');
  return response.json();
};

// Legal Analysis API helpers
export const extractClauses = async (documentContent, documentId = null, getAccessTokenSilently = null) => {
  let token = null;
  if (getAccessTokenSilently) {
    try {
      token = await getAccessTokenSilently({
        audience: 'https://legaldoc-api'
      });
    } catch (error) {
      throw new Error('Authentication required');
    }
  } else {
    token = getToken();
    if (!token) throw new Error('Authentication required');
  }
  
  const response = await fetch(`${baseURL}/api/legal/extract-clauses`, {
    method: 'POST',
    headers: { 
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}` 
    },
    body: JSON.stringify({ document_content: documentContent, document_id: documentId })
  });
  if (!response.ok) throw new Error((await response.json()).detail || 'Failed to extract clauses');
  return response.json();
};

export const checkCompliance = async (documentContent, jurisdiction = 'india', documentId = null, getAccessTokenSilently = null) => {
  let token = null;
  if (getAccessTokenSilently) {
    try {
      token = await getAccessTokenSilently({
        audience: 'https://legaldoc-api'
      });
    } catch (error) {
      throw new Error('Authentication required');
    }
  } else {
    token = getToken();
    if (!token) throw new Error('Authentication required');
  }

  const response = await fetch(`${baseURL}/api/legal/compliance-check`, {
    method: 'POST',
    headers: { 
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}` 
    },
    body: JSON.stringify({ 
      document_content: documentContent, 
      jurisdiction: jurisdiction,
      document_id: documentId 
    })
  });
  if (!response.ok) throw new Error((await response.json()).detail || 'Failed to check compliance');
  return response.json();
};

export const searchPrecedents = async (query, jurisdiction = 'india', documentType = null, getAccessTokenSilently = null) => {
  let token = null;
  if (getAccessTokenSilently) {
    try {
      token = await getAccessTokenSilently({
        audience: 'https://legaldoc-api'
      });
    } catch (error) {
      throw new Error('Authentication required');
    }
  } else {
    token = getToken();
    if (!token) throw new Error('Authentication required');
  }

  const response = await fetch(`${baseURL}/api/legal/precedent-search`, {
    method: 'POST',
    headers: { 
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}` 
    },
    body: JSON.stringify({ 
      query: query, 
      jurisdiction: jurisdiction,
      document_type: documentType 
    })
  });
  if (!response.ok) throw new Error((await response.json()).detail || 'Failed to search precedents');
  return response.json();
};

// PDF Text Extraction
export const extractPdfText = async (file) => {
  const token = getToken();
  if (!token) throw new Error('Authentication required');
  
  const formData = new FormData();
  formData.append('file', file);
  
  const response = await fetch(`${baseURL}/api/query/extract-pdf-text`, {
    method: 'POST',
    headers: { 'Authorization': `Bearer ${token}` },
    body: formData
  });
  if (!response.ok) throw new Error((await response.json()).detail || 'Failed to extract PDF text');
  return response.json();
};

// Chat Session API helpers
export const getChatSessions = async () => {
  const token = getToken();
  if (!token) throw new Error('Authentication required');
  
  const response = await fetch(`${baseURL}/api/chat/sessions`, {
    method: 'GET',
    headers: { 'Authorization': `Bearer ${token}` }
  });
  if (!response.ok) throw new Error((await response.json()).detail || 'Failed to fetch chat sessions');
  return response.json();
};

export const createChatSession = async (sessionName = null) => {
  const token = getToken();
  if (!token) throw new Error('Authentication required');
  
  const response = await fetch(`${baseURL}/api/chat/sessions`, {
    method: 'POST',
    headers: { 
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}` 
    },
    body: JSON.stringify({ session_name: sessionName })
  });
  if (!response.ok) throw new Error((await response.json()).detail || 'Failed to create chat session');
  return response.json();
};

export const deleteChatSession = async (sessionId) => {
  const token = getToken();
  if (!token) throw new Error('Authentication required');
  
  const response = await fetch(`${baseURL}/api/chat/sessions/${sessionId}`, {
    method: 'DELETE',
    headers: { 'Authorization': `Bearer ${token}` }
  });
  if (!response.ok) throw new Error((await response.json()).detail || 'Failed to delete chat session');
  return response.json();
};

export const getChatMessages = async (sessionId) => {
  const token = getToken();
  if (!token) throw new Error('Authentication required');
  
  const response = await fetch(`${baseURL}/api/chat/sessions/${sessionId}/messages`, {
    method: 'GET',
    headers: { 'Authorization': `Bearer ${token}` }
  });
  if (!response.ok) throw new Error((await response.json()).detail || 'Failed to fetch chat messages');
  return response.json();
};

export const createChatMessage = async (sessionId, messageType, content, sources = null, confidenceScore = null) => {
  const token = getToken();
  if (!token) throw new Error('Authentication required');
  
  const response = await fetch(`${baseURL}/api/chat/sessions/${sessionId}/messages`, {
    method: 'POST',
    headers: { 
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}` 
    },
    body: JSON.stringify({ 
      session_id: sessionId,
      message_type: messageType, 
      content: content,
      sources: sources,
      confidence_score: confidenceScore
    })
  });
  if (!response.ok) throw new Error((await response.json()).detail || 'Failed to create chat message');
  return response.json();
};

export const exportChatSession = async (sessionId, format = 'json') => {
  const token = getToken();
  if (!token) throw new Error('Authentication required');
  
  const response = await fetch(`${baseURL}/api/chat/sessions/${sessionId}/export?format=${format}`, {
    method: 'GET',
    headers: { 'Authorization': `Bearer ${token}` }
  });
  if (!response.ok) throw new Error((await response.json()).detail || 'Failed to export chat session');
  return response.json();
};

export default sendQuery;
