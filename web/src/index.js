import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';
import ThemeProvider from './ThemeProvider';
import { Auth0Provider } from '@auth0/auth0-react';

const root = ReactDOM.createRoot(document.getElementById('root'));

root.render(
  <Auth0Provider
  domain="dev-8oivjmih178u6qpg.us.auth0.com"
  clientId="USWlBGBM57kpWY8L5g1BTwYZ2uUArTAF"
  authorizationParams={{
    redirect_uri: window.location.origin,
    audience: "https://legaldoc-api"
  }}
  useRefreshTokens={true}
  cacheLocation="localstorage"
  >
    <React.StrictMode>
      <ThemeProvider>
        <React.Suspense fallback={
          <div className="flex items-center justify-center h-screen bg-slate-50 dark:bg-slate-900">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
          </div>
        }>
          <App />
        </React.Suspense>
      </ThemeProvider>
    </React.StrictMode>
  </Auth0Provider>
);
