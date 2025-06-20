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

export default sendQuery;