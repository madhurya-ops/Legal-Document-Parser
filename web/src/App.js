import React, { useState, useMemo, Suspense, lazy, useEffect } from "react";
// Lazy load heavy components
const FileUpload = lazy(() => import("./components/FileUpload"));
const ChatInterface = lazy(() => import("./components/ChatInterface"));
import ThemeToggle from "./components/ThemeToggle";
import { Card } from "./components/ui/card";
import { Badge } from "./components/ui/badge";
import { Scale, FileText, MessageSquare, X, Search, LogOut, Github, ArrowRight, Settings } from "lucide-react";
import "./App.css";
import AuthPage from "./components/AuthPage";
import HomePage from "./components/HomePage";
import AboutPage from "./components/AboutPage";
import AdminDashboard from "./components/AdminDashboard";
import EnhancedDashboard from "./components/EnhancedDashboard";
import { getToken, getCurrentUser, clearToken } from "./api";
import { Button } from "./components/ui/button";
import { useAuth0 } from "@auth0/auth0-react";

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
  const [showAdminDashboard, setShowAdminDashboard] = useState(false);
  const [activeTab, setActiveTab] = useState("Home");
  const { logout, isAuthenticated, user: auth0User, isLoading } = useAuth0();

  // Check authentication on mount and when auth state changes
  useEffect(() => {
    if (isLoading) {
      setAuthLoading(true);
      return;
    }
    
    if (isAuthenticated && auth0User) {
      // User is authenticated via Auth0
      setUser(auth0User);
      setShowHome(false);
      setShowAuth(false);
      setShowAbout(false);
      setAuthLoading(false);
    } else {
      // User is not authenticated
      setUser(null);
      setShowHome(true);
      setShowAuth(false);
      setShowAbout(false);
      setAuthLoading(false);
    }
  }, [isAuthenticated, auth0User, isLoading]);

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

  // Remove the old handleLogout function and replace with Auth0 logout
  const handleLogout = () => {
    logout({ logoutParams: { returnTo: window.location.origin } });
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

  // Add top padding only for non-chat pages
  const pageStyle = user ? {} : { paddingTop: '80px' };

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
            ) : showAdminDashboard && (user?.role === 'admin' || user?.role === 'ADMIN' || ['admin', 'admin1', 'admin2', 'admin3', 'admin4'].includes(user?.username)) ? (
              <AdminDashboard 
                user={user} 
                onClose={() => setShowAdminDashboard(false)} 
                onLogout={handleLogout}
              />
            ) : (
              <EnhancedDashboard
                user={user}
                uploadedFiles={uploadedFiles}
                selectedDocument={selectedDocument}
                searchQuery={searchQuery}
                filteredDocuments={filteredDocuments}
                messages={messages}
                setMessages={setMessages}
                handleFileUpload={handleFileUpload}
                removeFile={removeFile}
                setSelectedDocument={setSelectedDocument}
                setSearchQuery={setSearchQuery}
                handleLogout={handleLogout}
                setShowHome={setShowHome}
                setUser={setUser}
                setShowAuth={setShowAuth}
                setShowAbout={setShowAbout}
                setShowAdminDashboard={setShowAdminDashboard}
              />
            )}
          </div>
        </>
      )}
    </div>
  );
}