# Auth0 Integration Setup Guide

This guide will walk you through setting up Auth0 OAuth 2.0 + OpenID Connect authentication for your LegalDoc application.

## 1. Auth0 Dashboard Configuration

### Step 1: Create Auth0 Application
1. Log into your Auth0 Dashboard
2. Go to **Applications** → **Applications**
3. Click **Create Application**
4. Name: `LegalDoc Frontend`
5. Type: **Single Page Web Applications**
6. Click **Create**

### Step 2: Configure Application Settings
In your newly created application:

1. **Allowed Callback URLs**:
   ```
   http://localhost:3000/api/auth/callback,
   https://legal-document-parser.vercel.app/api/auth/callback
   ```

2. **Allowed Logout URLs**:
   ```
   http://localhost:3000,
   https://legal-document-parser.vercel.app
   ```

3. **Allowed Web Origins**:
   ```
   http://localhost:3000,
   https://legal-document-parser.vercel.app
   ```

4. **Advanced Settings** → **Grant Types**:
   - ✅ Authorization Code
   - ✅ Refresh Token
   - ✅ Implicit (for development only)

### Step 3: Create API
1. Go to **Applications** → **APIs**
2. Click **Create API**
3. **Name**: `LegalDoc API`
4. **Identifier**: `https://legaldoc-api`
5. **Signing Algorithm**: `RS256`
6. Click **Create**

### Step 4: Configure API Settings
1. In your API settings, go to **Machine to Machine Applications**
2. Authorize your SPA application if needed
3. Note down the **Identifier** (this is your `AUTH0_AUDIENCE`)

## 2. Environment Variables

### Frontend (Vercel)
Set these environment variables in your Vercel dashboard:

```env
AUTH0_SECRET=YOUR_RANDOM_32_CHAR_SECRET
AUTH0_BASE_URL=https://legal-document-parser.vercel.app
AUTH0_ISSUER_BASE_URL=https://YOUR_DOMAIN.auth0.com
AUTH0_CLIENT_ID=YOUR_SPA_CLIENT_ID
AUTH0_CLIENT_SECRET=YOUR_SPA_CLIENT_SECRET
AUTH0_AUDIENCE=https://legaldoc-api
```

### Backend (Render)
Set these environment variables in your Render dashboard:

```env
AUTH0_DOMAIN=YOUR_DOMAIN.auth0.com
AUTH0_AUDIENCE=https://legaldoc-api
```

## 3. Security Considerations

### Token Security
- ✅ Uses RS256 algorithm for secure token verification
- ✅ Validates `aud`, `iss`, `exp`, and `alg` claims
- ✅ JWKS endpoint caching with TTL
- ✅ Secure token transmission via HTTPS

### HTTPS Enforcement
Ensure your application runs over HTTPS in production:
- Vercel automatically provides HTTPS
- Render automatically provides HTTPS
- Local development can use HTTP

### Secret Rotation
- Rotate Auth0 secrets every 90 days
- Update environment variables across all deployments
- Monitor Auth0 logs for any suspicious activity

## 4. Testing the Integration

### 1. Test Protected Endpoint
```bash
# Get access token from frontend after login
curl -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
     https://legal-document-parser.onrender.com/api/auth/protected
```

### 2. Test User Creation
- First-time Auth0 login should automatically create user record
- Check `/api/auth/me` endpoint for user information

### 3. Test Admin Access
- Manually promote a user to admin in database
- Test admin endpoints with admin user token

## 5. Database Migration

Run the Auth0 migration script to update your database:

```bash
cd api
python migrate_auth0.py
```

This will:
- Add `auth0_sub` column to users table
- Create unique index on `auth0_sub`
- Make `hashed_password` nullable for Auth0 users

## 6. Deployment Steps

### Backend Deployment (Render)
1. Set Auth0 environment variables in Render dashboard
2. Deploy the updated code
3. Run database migration if needed
4. Test `/api/auth/protected` endpoint

### Frontend Deployment (Vercel)
1. Set Auth0 environment variables in Vercel dashboard
2. Deploy the updated frontend code
3. Test login/logout flow
4. Verify token is included in API requests

## 7. Monitoring and Maintenance

### Auth0 Dashboard Monitoring
- Monitor login/logout events
- Check for failed authentication attempts
- Review API usage statistics

### Application Logs
- Monitor backend logs for token validation errors
- Check for Auth0 JWKS fetch errors
- Watch for user creation/sync issues

### Regular Maintenance
- Review and rotate secrets quarterly
- Update Auth0 SDK versions regularly
- Monitor security advisories

## 8. Troubleshooting

### Common Issues

1. **Token Validation Fails**
   - Verify `AUTH0_DOMAIN` and `AUTH0_AUDIENCE` are correct
   - Check if JWKS endpoint is accessible
   - Ensure token hasn't expired

2. **User Creation Fails**
   - Check if email is present in token
   - Verify database connection
   - Check for username conflicts

3. **CORS Issues**
   - Verify allowed origins in Auth0 dashboard
   - Check CORS configuration in backend
   - Ensure frontend uses correct Auth0 callback URLs

### Debug Endpoints
- `/api/auth/token/info` - Debug token claims
- `/api/auth/health` - Check Auth0 system health
- `/api/debug/cors` - Check CORS configuration

## 9. Production Checklist

- [ ] Auth0 application configured with production URLs
- [ ] API configured with RS256 signing
- [ ] All environment variables set correctly
- [ ] Database migration completed
- [ ] HTTPS enforced across all endpoints
- [ ] Secrets rotated from defaults
- [ ] Error monitoring configured
- [ ] Auth0 logs monitoring setup
- [ ] Backup authentication method considered

## Support

For additional support:
- Auth0 Documentation: https://auth0.com/docs
- Auth0 Community: https://community.auth0.com
- FastAPI Documentation: https://fastapi.tiangolo.com
