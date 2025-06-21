// Sends a question to the FastAPI backend and returns the answer
export const sendQuery = async (payload) => {
  const baseURL = process.env.REACT_APP_API_URL || 'http://localhost:8000';
  try {
    const response = await fetch(`${baseURL}/ask`, {
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
    return 'Something went wrong while connecting to the server.';
  }
};

// Auth API helpers
const baseURL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

export const loginUser = async (email, password) => {
  const response = await fetch(`${baseURL}/auth/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password })
  });
  if (!response.ok) throw new Error((await response.json()).detail || 'Login failed');
  return response.json();
};

export const signupUser = async (username, email, password) => {
  const response = await fetch(`${baseURL}/auth/signup`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username, email, password })
  });
  if (!response.ok) throw new Error((await response.json()).detail || 'Signup failed');
  return response.json();
};

export const getCurrentUser = async (token) => {
  const response = await fetch(`${baseURL}/auth/me`, {
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