# Deployment Setup Guide

## Environment Variables Configuration

### For Vercel (Frontend) Deployment:

1. Go to your Vercel dashboard
2. Select your frontend project
3. Go to Settings → Environment Variables
4. Add the following environment variable:

**Name:** `REACT_APP_API_URL`
**Value:** `https://legaldoc-backend.onrender.com/api`
**Environment:** Production (and Preview if needed)

### For Render (Backend) Deployment:

1. Go to your Render dashboard
2. Select your backend service (`legaldoc-backend`)
3. Go to Environment → Environment Variables
4. Add the following environment variables:

**Required:**
- `GEMINI_API_KEY` - Your Gemini API key
- `SECRET_KEY` - A secure random string for JWT signing
- `DATABASE_URL` - Your database connection string

**Optional:**
- `HF_API_KEY` - Hugging Face API key (if using HF models)

## API Endpoints

Your backend will be available at:
- Base URL: `https://legaldoc-backend.onrender.com`
- API Base: `https://legaldoc-backend.onrender.com/api`
- Auth endpoints: 
  - `POST /api/auth/login`
  - `POST /api/auth/signup`
  - `GET /api/auth/me`

## Testing the Connection

After setting up the environment variables:

1. Deploy your backend on Render
2. Deploy your frontend on Vercel
3. Test the authentication endpoints

## Troubleshooting

If you get 404 errors:
1. Check that `REACT_APP_API_URL` is set correctly in Vercel
2. Verify your backend is running on Render
3. Check the Render logs for any startup errors
4. Ensure the `GEMINI_API_KEY` is set in your Render environment 