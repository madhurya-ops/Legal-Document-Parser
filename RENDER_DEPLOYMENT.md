# Render Deployment Guide

## Issue Resolution

The current deployment is failing because it's trying to connect to a local database container (`db:5432`) which doesn't exist on Render.

## Solution

### Option 1: Use Render's Blueprint (Recommended)

1. **Create a new Web Service on Render**
   - Connect your GitHub repository
   - Choose "Python" as the environment
   - Set the following configuration:

2. **Build Settings:**
   ```
   Build Command: pip install -r backend/requirements.txt
   Start Command: cd backend && python embeddings/embed_pdfs.py && uvicorn app.main:app --host 0.0.0.0 --port $PORT
   ```

3. **Environment Variables:**
   - `DATABASE_URL`: Will be provided by Render's PostgreSQL service
   - `SECRET_KEY`: Generate a secure random string
   - `HF_API_KEY`: Your Hugging Face API key

4. **Create a PostgreSQL Database:**
   - Create a new PostgreSQL service on Render
   - Copy the connection string to your web service's `DATABASE_URL` environment variable

### Option 2: Manual Deployment

1. **Create PostgreSQL Database:**
   - Go to Render Dashboard
   - Create a new PostgreSQL service
   - Note the connection string

2. **Create Web Service:**
   - Create a new Web Service
   - Connect your GitHub repo
   - Use the `render.yaml` configuration file

3. **Set Environment Variables:**
   - `DATABASE_URL`: Your PostgreSQL connection string
   - `SECRET_KEY`: A secure random string
   - `HF_API_KEY`: Your Hugging Face API key

### Option 3: Use Docker (Alternative)

If you prefer to use Docker:

1. **Update your deployment to use the production docker-compose:**
   ```bash
   docker-compose -f docker-compose.prod.yml up -d
   ```

2. **Set environment variables in Render:**
   - `DATABASE_URL`: Your external PostgreSQL connection string
   - `SECRET_KEY`: Secure random string
   - `HF_API_KEY`: Your Hugging Face API key

## Database Connection String Format

Your `DATABASE_URL` should look like:
```
postgresql://username:password@host:port/database_name
```

Example:
```
postgresql://legaldoc_user:password123@dpg-abc123-a.oregon-postgres.render.com/legaldoc_db
```

## Troubleshooting

1. **Database Connection Issues:**
   - Ensure `DATABASE_URL` is correctly set
   - Check that the database is accessible from your service
   - Verify network connectivity

2. **Port Issues:**
   - Render automatically sets the `$PORT` environment variable
   - Your app should listen on `0.0.0.0:$PORT`

3. **Health Check:**
   - The app now includes a `/health` endpoint
   - Render will use this to verify the service is running

## Next Steps

1. Create a PostgreSQL database on Render
2. Update your web service with the correct environment variables
3. Redeploy the application
4. Test the health endpoint: `https://your-app.onrender.com/health` 