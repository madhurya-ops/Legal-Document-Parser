// Utility script to test API connection
// Run this in browser console to debug API issues

export const testApiConnection = async () => {
  const apiUrl = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';
  console.log('Testing API connection to:', apiUrl);
  
  try {
    // Test health endpoint
    const healthResponse = await fetch(`${apiUrl.replace('/api', '')}/health`);
    console.log('Health check response:', healthResponse.status);
    
    // Test API base
    const apiResponse = await fetch(`${apiUrl}/auth/me`, {
      headers: {
        'Content-Type': 'application/json'
      }
    });
    console.log('API test response:', apiResponse.status);
    
    return {
      health: healthResponse.status,
      api: apiResponse.status,
      apiUrl
    };
  } catch (error) {
    console.error('API connection test failed:', error);
    return { error: error.message, apiUrl };
  }
};

// Usage: testApiConnection().then(console.log); # update Sun Jul  6 02:56:34 IST 2025
