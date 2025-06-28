import React, { useState, useMemo, Suspense, lazy, useEffect } from "react";
import { BrowserRouter as Router, Routes, Route, useNavigate, Navigate } from "react-router-dom";
// Lazy load heavy components
const FileUpload = lazy(() => import("./components/FileUpload"));
const ChatInterface = lazy(() => import("./components/ChatInterface"));
import ThemeToggle from "./components/ThemeToggle";
import { Card } from "./components/ui/card";
import { Badge } from "./components/ui/badge";
import { Scale, FileText, MessageSquare, X, Search, LogOut } from "lucide-react";
import "./App.css";
import AuthPage from "./components/AuthPage";
import HomePage from "./components/HomePage";
import { getToken, getCurrentUser, clearToken } from "./api";
import SignupPage from "./components/SignupPage";

export default function App() {
  const [uploadedFiles, setUploadedFiles] = useState([]);
  const [selectedDocument, setSelectedDocument] = useState(null);
  const [messages, setMessages] = useState([]);
  const [searchQuery, setSearchQuery] = useState("");
  const [user, setUser] = useState(null);
  const [authLoading, setAuthLoading] = useState(true);

  // Check authentication on mount
  useEffect(() => {
    const token = getToken();
    if (!token) {
      setAuthLoading(false);
      return;
    }
    getCurrentUser(token)
      .then((u) => {
        setUser(u);
      })
      .catch(() => {
        clearToken();
        setUser(null);
      })
      .finally(() => setAuthLoading(false));
  }, []);

  // Filter documents based on search query
  const filteredDocuments = useMemo(() => {
    if (!searchQuery.trim()) return uploadedFiles;
    return uploadedFiles.filter((file) => file.name.toLowerCase().includes(searchQuery.toLowerCase()));
  }, [uploadedFiles, searchQuery]);

  const handleFileUpload = (file) => {
    setUploadedFiles((prev) => [...prev, file]);
    setSelectedDocument(file);
  };

  const removeFile = (index) => {
    setUploadedFiles((prev) => prev.filter((_, i) => i !== index));
    if (selectedDocument === uploadedFiles[index]) {
      setSelectedDocument(null);
    }
  };

  const handleLogout = () => {
    clearToken();
    setUser(null);
  };

  const handleAuthSuccess = (userData) => {
    setUser(userData);
  };

  // Persist chat messages in localStorage
  useEffect(() => {
    if (user) {
      localStorage.setItem('chat_messages', JSON.stringify(messages));
    }
  }, [messages, user]);

  useEffect(() => {
    if (user) {
      const saved = localStorage.getItem('chat_messages');
      if (saved) {
        try {
          setMessages(JSON.parse(saved));
        } catch {}
      }
    }
  }, [user]);

  if (authLoading) {
    return (
      <div className="flex items-center justify-center h-screen bg-slate-50 dark:bg-slate-900">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  return (
    <Router>
      <Routes>
        <Route path="/" element={<HomePage onGetStarted={() => window.location.href = '/login'} />} />
        <Route path="/login" element={<AuthPage onAuthSuccess={handleAuthSuccess} onBack={() => window.location.href = '/'} />} />
        <Route path="/signup" element={<SignupPage />} />
        <Route path="/chat" element={
          user ? (
            <div className="min-h-screen bg-slate-50 dark:bg-slate-900 bg-dots relative overflow-hidden">
              {/* Header */}
              <header className="fixed left-0 top-0 w-full z-50 flex items-center justify-between px-2 sm:px-4 md:px-16 py-3 sm:py-4 bg-white/90 dark:bg-slate-900/90 backdrop-blur-lg shadow-2xl border border-slate-200/60 dark:border-slate-700/60 rounded-b-2xl">
                {/* Left side */}
                <div className="flex items-center gap-2">
                  <ThemeToggle />
                  <button
                    onClick={handleLogout}
                    className="inline-flex items-center gap-2 px-4 py-2 rounded-xl border border-red-600 dark:border-red-400 text-red-700 dark:text-red-300 font-semibold bg-white/90 dark:bg-slate-900/90 hover:bg-red-50 dark:hover:bg-red-800/40 transition-all duration-300 shadow-md text-base"
                  >
                    <LogOut className="w-4 h-4" /> Logout
                  </button>
                </div>
                
                {/* Centered logo - positioned relative to page */}
                <div className="absolute left-1/2 transform -translate-x-1/2 flex items-center gap-3">
                  <Scale className="w-8 h-8 text-blue-600 dark:text-blue-400" />
                  <span className="text-2xl font-bold text-slate-900 dark:text-slate-100">LegalDoc</span>
                </div>
                
                {/* Right side */}
                <div className="flex items-center gap-2">
                  <span className="text-sm text-slate-600 dark:text-slate-400">Welcome, {user?.username}</span>
                </div>
              </header>

              {/* Main content */}
              <div className="pt-20 h-screen flex">
                {/* File upload sidebar */}
                <div className="w-80 p-4 border-r border-slate-200 dark:border-slate-700 bg-white/90 dark:bg-slate-800/90 backdrop-blur-sm">
                  <div className="space-y-4">
                    <div className="flex items-center justify-between">
                      <h2 className="text-lg font-semibold text-slate-900 dark:text-slate-100">Documents</h2>
                      <Search className="w-5 h-5 text-slate-400" />
                    </div>
                    
                    {/* Search input */}
                    <input
                      type="text"
                      placeholder="Search documents..."
                      value={searchQuery}
                      onChange={(e) => setSearchQuery(e.target.value)}
                      className="w-full px-3 py-2 rounded-lg border border-slate-300 dark:border-slate-600 bg-white/80 dark:bg-slate-800/80 text-slate-900 dark:text-slate-100 placeholder:text-slate-500 dark:placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-blue-400 dark:focus:ring-blue-500 transition-colors duration-300"
                    />
                    
                    {/* File upload */}
                    <Suspense fallback={<div className="animate-pulse h-32 bg-slate-200 dark:bg-slate-700 rounded-lg"></div>}>
                      <FileUpload onFileUpload={handleFileUpload} selectedDocument={selectedDocument} boxSize="small" />
                    </Suspense>
                    
                    {/* Document list */}
                    <div className="space-y-2">
                      {filteredDocuments.map((file, index) => (
                        <Card key={index} className={`p-3 cursor-pointer transition-all duration-300 hover:shadow-md ${selectedDocument === file ? 'ring-2 ring-blue-400 bg-blue-50 dark:bg-blue-900/20' : ''}`} onClick={() => setSelectedDocument(file)}>
                          <div className="flex items-center justify-between">
                            <div className="flex items-center gap-2">
                              <FileText className="w-4 h-4 text-blue-600 dark:text-blue-400" />
                              <span className="text-sm font-medium text-slate-900 dark:text-slate-100 truncate">{file.name}</span>
                            </div>
                            <button
                              onClick={(e) => { e.stopPropagation(); removeFile(index); }}
                              className="p-1 hover:bg-red-100 dark:hover:bg-red-900/30 rounded transition-colors duration-200"
                            >
                              <X className="w-3 h-3 text-red-500" />
                            </button>
                          </div>
                        </Card>
                      ))}
                    </div>
                  </div>
                </div>
                
                {/* Chat interface */}
                <div className="flex-1">
                  <Suspense fallback={<div className="flex items-center justify-center h-full"><div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div></div>}>
                    <ChatInterface uploadedFile={selectedDocument} messages={messages} setMessages={setMessages} />
                  </Suspense>
                </div>
              </div>
            </div>
          ) : (
            <Navigate to="/login" replace />
          )
        } />
        <Route path="*" element={<Navigate to="/" />} />
      </Routes>
    </Router>
  );
}