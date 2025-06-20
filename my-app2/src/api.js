import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000', // Adjust if FastAPI is running elsewhere
  headers: {
    'Content-Type': 'application/json',
  },
});

// Sends a question to the FastAPI backend and returns the answer
export const sendQuery = async (question) => {
  try {
    const response = await api.post('/ask', { question });
    if (response.data && response.data.answer) {
      return response.data.answer;
    } else {
      return 'No answer returned from server.';
    }
  } catch (error) {
    console.error('❌ Error querying backend:', error);
    if (error.response && error.response.data?.detail) {
      return `Server error: ${error.response.data.detail}`;
    }
    return 'Something went wrong while connecting to the server.';
  }
};

export default api;