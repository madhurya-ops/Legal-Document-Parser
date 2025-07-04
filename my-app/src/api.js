// Configuration from environment variables
const API_CONFIG = {
  baseURL: (process.env.REACT_APP_API_URL || (window.location.hostname === 'localhost' && window.location.port === '3000' ? '' : 'http://localhost:8000')).replace(/\/+$/, ''),
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
export const sendQuery = async (payload) => {
  try {
    const response = await fetchWithRetry(`${API_CONFIG.baseURL}/api/ask`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
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
const baseURL = (process.env.REACT_APP_API_URL || (window.location.hostname === 'localhost' && window.location.port === '3000' ? '' : 'http://localhost:8000')).replace(/\/+$/, '');

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

export function storeToken(token) {
  localStorage.setItem('access_token', token);
}
export function getToken() {
  return localStorage.getItem('access_token');
}
export function clearToken() {
  localStorage.removeItem('access_token');
}

export default sendQuery;