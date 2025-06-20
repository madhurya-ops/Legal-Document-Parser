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
<<<<<<< HEAD
    const response = await api.post('/ask', { question });
    if (response.data && response.data.answer) {
      return response.data.answer;
=======
    const response = await api.post('/ask', payload);
    if (response.data && typeof response.data === 'object') {
      if ('answer' in response.data) {
        return response.data.answer;
      } else {
        return JSON.stringify(response.data);
      }
>>>>>>> 5721d64 (Added functional dynamic Frontend integrated with Backend.)
    } else {
      return String(response.data);
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