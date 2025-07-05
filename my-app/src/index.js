import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';
import ThemeProvider from './ThemeProvider';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <ThemeProvider>
      <React.Suspense fallback={<div className="flex items-center justify-center h-screen bg-slate-50 dark:bg-slate-900"><div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div></div>}>
        <App />
      </React.Suspense>
    </ThemeProvider>
  </React.StrictMode>
);
# update Sun Jul  6 02:56:34 IST 2025
