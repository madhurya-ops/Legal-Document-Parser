import React, { useState, useMemo, Suspense, lazy, useEffect } from "react";
// Lazy load heavy components
const FileUpload = lazy(() => import("./components/FileUpload"));
const ChatInterface = lazy(() => import("./components/ChatInterface"));
import ThemeToggle from "./components/ThemeToggle";
import { Card } from "./components/ui/card";
import { Badge } from "./components/ui/badge";
import { Scale, FileText, MessageSquare, X, Search, LogOut, Github, ArrowRight } from "lucide-react";
import "./App.css";
import AuthPage from "./components/AuthPage";
import HomePage from "./components/HomePage";
import AboutPage from "./components/AboutPage";
import { getToken, getCurrentUser, clearToken } from "./api";
import { Button } from "./components/ui/button";

const tabs = [
  "Home",
  "Features",
  "Why Use LegalDoc",
  "Tech Stack",
  "FAQs",
  "About"
];

export default function App() {
  const [uploadedFiles, setUploadedFiles] = useState([]);
  const [selectedDocument, setSelectedDocument] = useState(null);
  const [messages, setMessages] = useState([]);
  const [searchQuery, setSearchQuery] = useState("");
  const [user, setUser] = useState(null);
  const [authLoading, setAuthLoading] = useState(true);
  const [showAuth, setShowAuth] = useState(false);
  const [showHome, setShowHome] = useState(true);
  const [showAbout, setShowAbout] = useState(false);
  const [activeTab, setActiveTab] = useState("Home");

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
        setShowHome(false);
      })
      .catch(() => {
        clearToken();
        setUser(null);
        setShowHome(true);
      })
      .finally(() => setAuthLoading(false));
  }, []);

  // Filter documents based on search query
  const filteredDocuments = useMemo(() => {
    if (!searchQuery.trim()) return uploadedFiles;
    return uploadedFiles.filter((file) => file.name.toLowerCase().includes(searchQuery.toLowerCase()));
  }, [uploadedFiles, searchQuery]);

  const handleFileUpload = (file, uploadResult) => {
    // Store file with upload result from backend
    const fileWithResult = { ...file, uploadResult };
    setUploadedFiles((prev) => [...prev, fileWithResult]);
    setSelectedDocument(fileWithResult);
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
    setShowHome(true);
    setShowAuth(false);
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

  const handleShowAbout = () => {
    setShowAbout(true);
    setShowHome(false);
    setShowAuth(false);
    setTimeout(() => { window.scrollTo({ top: 0, behavior: 'smooth' }); }, 10);
  };

  const handleShowHome = () => {
    setShowAbout(false);
    setShowHome(true);
    setShowAuth(false);
    setTimeout(() => { window.scrollTo({ top: 0, behavior: 'smooth' }); }, 10);
  };

  // Helper to scroll to a section by tab name
  function scrollToSection(tab) {
    const sectionMap = {
      "Home": "home",
      "Features": "features",
      "Why Use LegalDoc": "whyuselegaldoc",
      "Tech Stack": "techstack",
      "FAQs": "faqs"
    };
    const id = sectionMap[tab] || sectionMap[tab.replace(/ /g, '')];
    if (id) {
      const el = document.getElementById(id);
      if (el) {
        const y = el.getBoundingClientRect().top + window.scrollY - 80;
        window.scrollTo({ top: y, behavior: 'smooth' });
      }
    }
  }

  // Header always visible
  const renderHeader = () => (
    <header className="fixed top-0 left-0 w-full z-50 flex items-center justify-between px-2 sm:px-6 md:px-16 py-3 sm:py-4 bg-background/90 backdrop-blur-lg shadow-2xl border-b border-border animate-fade-in-up">
      {/* Logo (left) */}
      <div className="flex items-center gap-3">
        <button
          className="flex items-center gap-3 focus:outline-none hover:scale-105 transition-transform duration-200"
          onClick={() => { setActiveTab('Home'); handleShowHome(); }}
          title="About LegalDoc"
          aria-label="About LegalDoc"
          tabIndex={-1}
        >
          <Scale className="w-8 h-8 text-primary" />
          <span className="text-2xl font-bold text-foreground">LegalDoc</span>
        </button>
      </div>
      {/* Tabs (center, horizontal) */}
      <nav className="flex-1 flex justify-center gap-2 sm:gap-4">
        {tabs.map((tab) => (
          <Button
            key={tab}
            variant={tab === (showAbout ? "About" : activeTab) ? "default" : "ghost"}
            className={`rounded-xl px-4 py-2 text-base font-semibold transition-all duration-200 fade-in-up-delay-1 ${tab === (showAbout ? "About" : activeTab) ? "bg-primary text-primary-foreground" : "text-foreground hover:bg-muted/60"}`}
            onClick={() => {
              if (tab === "About") {
                handleShowAbout();
              } else {
                setActiveTab(tab);
                // Only switch to home if not already there
                if (!showHome) {
                  handleShowHome();
                  setTimeout(() => {
                    scrollToSection(tab);
                  }, 20);
                } else {
                  scrollToSection(tab);
                }
              }
            }}
            aria-current={tab === (showAbout ? "About" : activeTab) ? "page" : undefined}
          >
            {tab}
          </Button>
        ))}
      </nav>
      {/* Right side controls */}
      <div className="flex items-center gap-2 fade-in-up-delay-2">
        <ThemeToggle />
        <a
          href="https://github.com/madhurya-ops/Legal-Document-Parser"
          target="_blank"
          rel="noopener noreferrer"
          className="inline-flex items-center gap-2 px-4 py-2 rounded-xl border border-primary text-primary font-semibold bg-background/90 hover:bg-primary/10 transition-all duration-300 shadow-md text-base hover-lift"
          tabIndex={0}
          aria-label="GitHub Repository"
        >
          <Github className="w-5 h-5" /> GitHub
        </a>
        <Button
          className="px-4 py-2 rounded-xl text-base font-semibold hover-lift fade-in-up-delay-3"
          onClick={() => { setShowAuth(true); setShowHome(false); setShowAbout(false); }}
        >
          Get Started
          <ArrowRight className="ml-2 w-5 h-5" />
        </Button>
      </div>
    </header>
  );

  if (authLoading) {
    return (
      <div className="flex items-center justify-center h-screen bg-background text-foreground">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div>
      </div>
    );
  }

  // Add top padding to account for fixed header height (e.g., 80px)
  const pageStyle = { paddingTop: '80px' };

  return (
    <div>
      {showAuth && !user ? (
        <div className="min-h-screen flex flex-col md:flex-row">
          {/* Branding/opaque left side */}
          <div className="hidden md:flex flex-col items-center w-1/2 bg-background p-0 shadow-lg shadow-slate-300/40 dark:shadow-slate-900/60 border-r border-border z-10">
            {/* Header */}
            <div className="w-full flex flex-col items-center pt-16 pb-2 px-8">
              <Scale className="w-16 h-16 text-foreground mb-4" />
              <h1 className="text-4xl font-extrabold text-foreground mb-2">LegalDoc</h1>
              <p className="text-lg text-muted-foreground mb-4 text-center">AI-powered legal document analysis</p>
              {/* Body content, close to header */}
              <p className="text-base text-muted-foreground text-center max-w-md mb-2">Upload, parse, and understand legal documents with instant AI analysis, summaries, and insights. Secure, private, and easy to use.</p>
            </div>
            <div className="flex-1" />
            {/* Footer */}
            <footer className="w-full py-6 px-8 text-center text-muted-foreground text-sm border-t border-border/60 mt-auto">
              <div className="flex flex-col items-center gap-2">
                <span>&copy; {new Date().getFullYear()} LegalDoc. All rights reserved.</span>
                <a href="mailto:bansalchaitanya1234@gmail.com" className="hover:underline text-foreground">Contact</a>
              </div>
            </footer>
          </div>
          {/* Auth form right side */}
          <div className="w-1/2 flex items-center justify-center bg-background bg-dots">
            <AuthPage
              cardSize="xxl"
              onAuthSuccess={(u) => { setUser(u); setShowAuth(false); setShowHome(false); setShowAbout(false); }}
              onBack={() => { setShowHome(true); setShowAuth(false); setShowAbout(false); }}
            />
          </div>
        </div>
      ) : (
        <>
          {/* Only render header on non-chat pages */}
          {(!user) && renderHeader()}
          <div style={pageStyle}>
            {showAbout ? (
              <AboutPage
                onGetStarted={() => { setShowAuth(true); setShowHome(false); setShowAbout(false); }}
                activeTab={activeTab}
                onTabChange={(tab) => {
                  if (tab === "About") return;
                  setActiveTab(tab); setShowAbout(false); setShowHome(true); setShowAuth(false);
                }}
              />
            ) : showHome && !user ? (
              <HomePage
                onGetStarted={() => { setShowAuth(true); setShowHome(false); setShowAbout(false); }}
                activeTab={activeTab}
                setActiveTab={setActiveTab}
              />
            ) : !user ? (
              <HomePage
                onGetStarted={() => { setShowAuth(true); setShowHome(false); setShowAbout(false); }}
                activeTab={activeTab}
                setActiveTab={setActiveTab}
              />
            ) : (
              <div className="flex h-screen bg-background text-foreground transition-colors duration-300 fade-in-home overflow-hidden">
                {/* Sidebar (left) */}
                <div className="w-80 flex flex-col h-full border-r border-border bg-background/90 bg-dots shadow-2xl z-10">
                  {/* Sidebar Header: Logo, Back, Theme */}
                  <div className="flex items-center justify-between gap-2 px-4 pt-6 pb-4 border-b border-border bg-background/95">
                    <div className="flex items-center gap-2">
                      <button
                        className="p-2 rounded-full bg-background/80 border border-border shadow hover:bg-primary/10 transition-colors"
                        onClick={() => { setShowHome(true); setUser(null); setShowAuth(false); setShowAbout(false); }}
                        title="Back to Home"
                        aria-label="Back to Home"
                      >
                        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2" className="text-primary"><path strokeLinecap="round" strokeLinejoin="round" d="M15 19l-7-7 7-7" /></svg>
                      </button>
                      <Scale className="w-7 h-7 text-primary" />
                      <span className="text-xl font-bold text-foreground">LegalDoc</span>
                    </div>
                    <ThemeToggle />
                  </div>
                  {/* UploadBox (fixed, not scrollable) */}
                  <div className="p-4 border-b border-border bg-background/95">
                    <Suspense fallback={<div>Loading upload...</div>}>
                      <FileUpload onFileUpload={handleFileUpload} selectedDocument={selectedDocument} boxSize="small" />
                    </Suspense>
                  </div>
                  {/* Document List (scrollable) */}
                  <div className="flex-1 flex flex-col overflow-y-auto min-h-0 p-4">
                    <div className="mb-2">
                      <div className="relative mb-2">
                        <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground" />
                        <input
                          type="text"
                          placeholder="Search documents..."
                          value={searchQuery}
                          onChange={(e) => setSearchQuery(e.target.value)}
                          className="pl-9 pr-3 py-2 w-full rounded-md border border-border bg-background/80 text-sm text-foreground focus:outline-none focus:ring-2 focus:ring-primary placeholder:text-muted-foreground"
                        />
                      </div>
                      <h3 className="text-sm font-medium text-muted-foreground mb-2">
                        Documents ({uploadedFiles.length})
                      </h3>
                    </div>
                    <div className="space-y-3">
                      {filteredDocuments.length === 0 ? (
                        <div className="text-center py-8">
                          <FileText className="h-8 w-8 text-muted-foreground mx-auto mb-2" />
                          <p className="text-sm text-muted-foreground">No documents uploaded</p>
                        </div>
                      ) : (
                        filteredDocuments.map((file, index) => (
                          <Card
                            key={index}
                            className={`p-3 hover:bg-muted cursor-pointer transition-colors flex items-center justify-between mb-2 ${selectedDocument === file ? 'ring-2 ring-primary bg-primary/10' : ''}`}
                            onClick={() => setSelectedDocument(file)}
                          >
                            <div className="flex items-center gap-2 flex-1 min-w-0">
                              <FileText className="h-4 w-4 text-primary flex-shrink-0" />
                              <div className="min-w-0 flex-1">
                                <p className="text-sm font-medium text-foreground truncate">{file.name}</p>
                                <p className="text-xs text-muted-foreground">
                                  {(file.size / 1024 / 1024).toFixed(2)} MB
                                </p>
                              </div>
                            </div>
                            <button
                              onClick={e => { e.stopPropagation(); removeFile(index); }}
                              className="h-6 w-6 flex items-center justify-center p-0 rounded hover:bg-primary/10 transition-colors"
                              title="Remove"
                            >
                              <X className="h-4 w-4 text-primary m-auto" />
                            </button>
                          </Card>
                        ))
                      )}
                    </div>
                  </div>
                </div>
                {/* Main Content Area (Chat) */}
                <div className="flex-1 flex flex-col h-full bg-background text-foreground relative">
                  <div className="flex-1 min-h-0 flex flex-col fade-in-chat">
                    <Suspense fallback={<div>Loading chat...</div>}>
                      <ChatInterface
                        uploadedFile={selectedDocument}
                        messages={messages}
                        setMessages={setMessages}
                      />
                    </Suspense>
                  </div>
                </div>
              </div>
            )}
          </div>
        </>
      )}
    </div>
  );
}