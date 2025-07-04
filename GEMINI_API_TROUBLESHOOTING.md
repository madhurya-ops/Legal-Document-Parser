# Gemini API Troubleshooting Guide

## Issue: 429 Too Many Requests Error

The 429 error typically occurs due to rate limiting on the Gemini API. Here are several solutions to try:

## 1. API URL Options

Try these different Gemini API endpoints in your `.env` file:

### Option 1: Current (Latest Model)
```bash
GEMINI_API_URL=https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent
```

### Option 2: Specific Version
```bash
GEMINI_API_URL=https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent
```

### Option 3: V1 API (Non-beta)
```bash
GEMINI_API_URL=https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent
```

### Option 4: Alternative Model
```bash
GEMINI_API_URL=https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent
```

## 2. Rate Limiting Configuration

Adjust these settings in your `.env` file to reduce API calls:

```bash
# Reduce request frequency
REQUEST_TIMEOUT=45
RATE_LIMIT_RETRY_DELAY=120
MAX_RETRIES=2

# Reduce token usage
MAX_OUTPUT_TOKENS=300
CONTEXT_TRUNCATION_LIMIT=2000
PROMPT_TRUNCATION_LIMIT=600
RESPONSE_LIMIT=600
```

## 3. API Key Management

### Check API Key Status
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Verify your API key is active
3. Check usage quotas and limits

### Generate New API Key
If the current key has exceeded limits:
1. Create a new API key
2. Update `GEMINI_API_KEY` in `.env`
3. Restart the application

## 4. Request Optimization

The application now includes:
- ✅ **Automatic retry logic** for 429 errors
- ✅ **Exponential backoff** with configurable delays
- ✅ **Request limiting** to prevent rapid API calls
- ✅ **Error handling** with user-friendly messages

## 5. Testing Commands

### Test API Connection
```bash
# Check if backend is running
curl http://localhost:8000/health

# Test with a simple query
curl -X POST http://localhost:8000/api/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "Hello"}'
```

### Monitor Logs
```bash
# Watch backend logs for API errors
docker compose logs -f backend

# Check for rate limit messages
docker compose logs backend | grep -i "rate limit"
```

## 6. Alternative Solutions

### Option A: Use Different Model
Try switching to a different Gemini model that might have different rate limits:

```bash
# In .env file
GEMINI_API_URL=https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent
```

### Option B: Implement Request Queuing
For high-volume usage, consider implementing a request queue to space out API calls.

### Option C: Upgrade API Plan
Consider upgrading to a paid Google Cloud plan for higher rate limits.

## 7. Current Implementation Features

The updated LLM client now includes:

### Rate Limit Handling
- **3 automatic retries** with increasing delays
- **60-second wait** between retries for 429 errors
- **Graceful fallback** messages for users

### Error Messages
- Rate limit exceeded: "Rate limit exceeded. Please try again later or check your API usage."
- Timeout: "Request timed out after multiple attempts. Please try again later."
- General error: "Failed to get response after multiple attempts. Please try again later."

### Configurable Settings
All timing and retry settings can be adjusted via environment variables without code changes.

## 8. Quick Fix Commands

### Restart with New Settings
```bash
# After updating .env file
docker compose down
docker compose up --build -d
```

### Check Current Configuration
```bash
# View current environment settings
docker compose exec backend env | grep GEMINI
```

## 9. Best Practices

1. **Monitor Usage**: Keep track of your API usage to avoid hitting limits
2. **Batch Requests**: Group multiple questions into single requests when possible
3. **Cache Responses**: Store frequently requested analysis results
4. **Optimize Prompts**: Use shorter, more focused prompts to reduce token usage
5. **User Feedback**: Inform users about rate limits and expected wait times

## 10. Support Resources

- **Google AI Studio**: https://makersuite.google.com/
- **Gemini API Documentation**: https://ai.google.dev/docs
- **Rate Limits Info**: https://ai.google.dev/docs/gemini_api_overview#rate-limits

---

If you continue to experience issues after trying these solutions, the problem might be:
1. API key quota exhaustion
2. Regional restrictions
3. Temporary Google API issues

Consider generating a new API key or waiting 24 hours for quota reset.
