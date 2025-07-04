import React, { useState, Suspense } from "react";
import { Card } from "./ui/card";
import { Button } from "./ui/button";
import { Badge } from "./ui/badge";
import ThemeToggle from "./ThemeToggle";
import ChatInterface from "./ChatInterface";
import FileUpload from "./FileUpload";
import ChatHistoryPanel from "./ChatHistoryPanel";
import AIToolsPanel from "./AIToolsPanel";
import LanguageSelector from "./LanguageSelector";
import TemplateSelector from "./TemplateSelector";
import ProfileSettings from "./ProfileSettings";
import {
  Scale,
  FileText,
  X,
  Search,
  LogOut,
  Settings,
  User,
  History,
  ChevronLeft,
  ChevronRight,
  MessageSquare,
  Bot
} from "lucide-react";

const EnhancedDashboard = ({
  user,
  uploadedFiles,
  selectedDocument,
  searchQuery,
  filteredDocuments,
  messages,
  setMessages,
  handleFileUpload,
  removeFile,
  setSelectedDocument,
  setSearchQuery,
  handleLogout,
  setShowHome,
  setUser,
  setShowAuth,
  setShowAbout,
  setShowAdminDashboard
}) => {
  const [showChatHistory, setShowChatHistory] = useState(false);
  const [showProfile, setShowProfile] = useState(false);
  const [showAITools, setShowAITools] = useState(false);
  const [showTemplates, setShowTemplates] = useState(false);
  const [chatSessions, setChatSessions] = useState([
    { id: 1, name: 'New Chat', messages: [], lastMessage: '', timestamp: new Date() }
  ]);
  const [currentChatId, setCurrentChatId] = useState(1);

  const handleBackToHome = () => {
    setShowHome(true);
    setUser(null);
    setShowAuth(false);
    setShowAbout(false);
  };

  const handleNewChat = () => {
    const newId = Math.max(...chatSessions.map(s => s.id)) + 1;
    const newSession = {
      id: newId,
      name: `Chat ${newId}`,
      messages: [],
      lastMessage: '',
      timestamp: new Date()
    };
    setChatSessions([newSession, ...chatSessions]);
    setCurrentChatId(newId);
    setMessages([]);
  };

  const handleChatSelect = (chatId) => {
    setCurrentChatId(chatId);
    const chat = chatSessions.find(s => s.id === chatId);
    setMessages(chat?.messages || []);
    setShowChatHistory(false);
  };

  // Save messages to current chat session
  React.useEffect(() => {
    setChatSessions(prev => prev.map(session => 
      session.id === currentChatId 
        ? { ...session, messages, lastMessage: messages[messages.length - 1]?.content || '' }
        : session
    ));
  }, [messages, currentChatId]);

  return (
    <div className="flex h-screen bg-background bg-dots text-foreground transition-colors duration-300 fade-in-home overflow-hidden">
      {/* Chat History Slide-out Panel */}
      <ChatHistoryPanel 
        isOpen={showChatHistory}
        onClose={() => setShowChatHistory(false)}
        chatSessions={chatSessions}
        currentChatId={currentChatId}
        onChatSelect={handleChatSelect}
        onNewChat={handleNewChat}
      />

      {/* Profile Settings Modal */}
      <ProfileSettings 
        isOpen={showProfile}
        onClose={() => setShowProfile(false)}
        user={user}
        onSave={(data) => {
          console.log('Profile updated:', data);
          // Here you would update the user data
        }}
      />

      {/* Left Panel - Floating with curved edges */}
      <div className="w-72 flex flex-col h-full p-4 z-20 relative">
        {/* Main Left Panel Card */}
        <Card className="flex-1 flex flex-col bg-background/95 backdrop-blur-lg border border-border/50 shadow-2xl rounded-3xl overflow-hidden hover-glow">
            {/* Header with Branding */}
            <div className="px-6 pt-6 pb-4 border-b border-border/20">
              <div className="flex items-center justify-between mb-6">
                <div className="flex items-center gap-3">
                  <div className="p-2.5 bg-primary/10 rounded-xl">
                    <Scale className="w-6 h-6 text-primary" />
                  </div>
                  <div>
                    <span className="text-lg font-bold text-foreground">LegalDoc</span>
                    <p className="text-xs text-muted-foreground">Document Analysis</p>
                  </div>
                </div>
                <ThemeToggle />
              </div>
          
            {/* User Info */}
            <div className="flex items-center gap-3 mb-6 p-3 bg-muted/30 rounded-xl">
              <div className="w-9 h-9 rounded-full bg-gradient-to-br from-primary to-primary/60 flex items-center justify-center">
                <span className="text-sm font-medium text-primary-foreground">
                  {user?.username?.charAt(0)?.toUpperCase() || 'U'}
                </span>
              </div>
              <div className="flex-1 min-w-0">
                <p className="text-sm font-medium text-foreground truncate">
                  {user?.username || 'User'}
                </p>
                <p className="text-xs text-muted-foreground truncate">
                  {user?.email || ''}
                </p>
              </div>
            </div>

            {/* Action Buttons - Only 3 buttons */}
            <div className="flex items-center justify-center gap-2">
              <Button
                variant="ghost"
                size="icon"
                onClick={() => setShowProfile(!showProfile)}
                className="rounded-full border border-border bg-background/90 hover:bg-muted transition-all duration-300 shadow-sm hover:shadow-md hover:scale-105 active:scale-95"
                title="Account Details"
              >
                <User className="w-5 h-5" />
              </Button>
              
              <Button
                variant="ghost"
                size="icon"
                onClick={() => setShowChatHistory(!showChatHistory)}
                className="rounded-full border border-border bg-background/90 hover:bg-muted transition-all duration-300 shadow-sm hover:shadow-md hover:scale-105 active:scale-95"
                title="Chat History"
              >
                <History className="w-5 h-5" />
              </Button>
              
              <Button
                variant="ghost"
                size="icon"
                onClick={handleLogout}
                className="rounded-full border border-border bg-background/90 hover:bg-muted transition-all duration-300 shadow-sm hover:shadow-md hover:scale-105 active:scale-95 text-destructive"
                title="Sign Out"
              >
                <LogOut className="w-5 h-5" />
              </Button>
            </div>
        </div>

          {/* Document Upload */}
          <div className="p-4 border-b border-border/20">
            <h3 className="text-xs font-semibold text-foreground mb-2 flex items-center gap-2">
              <FileText className="w-4 h-4 text-primary" />
              Upload Legal Document
            </h3>
            <Suspense fallback={<div className="text-sm text-muted-foreground">Loading upload...</div>}>
              <FileUpload 
                onFileUpload={handleFileUpload} 
                selectedDocument={selectedDocument} 
                boxSize="small" 
              />
            </Suspense>
          </div>

          {/* Document List */}
          <div className="flex-1 flex flex-col p-4 min-h-0">
            <div className="mb-3">
              <div className="relative mb-3">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground" />
                <input
                  type="text"
                  placeholder="Search documents..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="pl-9 pr-3 py-2 w-full rounded-lg border border-border/50 bg-background/50 text-sm text-foreground focus:outline-none focus:ring-2 focus:ring-primary/20 focus:border-primary placeholder:text-muted-foreground transition-all"
                />
              </div>
              <div className="flex items-center justify-between mb-3">
                <h3 className="text-xs font-semibold text-foreground">
                  Documents ({uploadedFiles.length})
                </h3>
                <Badge variant="secondary" className="text-sm px-2 py-1">
                  {uploadedFiles.length}
                </Badge>
              </div>
            </div>
          
            {/* Scrollable document list - Takes remaining space */}
            <div className="flex-1 overflow-y-auto pr-1 scrollbar-thin scrollbar-thumb-border scrollbar-track-transparent">
              <div className="space-y-2">
                {filteredDocuments.length === 0 ? (
                  <div className="text-center py-6">
                    <div className="p-3 bg-muted/30 rounded-lg mb-3 mx-auto w-12 h-12 flex items-center justify-center">
                      <FileText className="h-6 w-6 text-muted-foreground" />
                    </div>
                    <p className="text-sm text-muted-foreground">No documents uploaded</p>
                    <p className="text-sm text-muted-foreground mt-1 opacity-70">Upload to get started</p>
                  </div>
                ) : (
                  filteredDocuments.map((file, index) => (
                    <Card
                      key={index}
                      className={`p-3 hover:bg-muted/50 cursor-pointer transition-all hover:shadow-sm flex items-center justify-between rounded-lg border-border/30 ${
                        selectedDocument === file ? 'ring-1 ring-primary bg-primary/10 shadow-sm border-primary/50' : 'hover:border-border/60'
                      }`}
                      onClick={() => setSelectedDocument(file)}
                    >
                      <div className="flex items-center gap-3 flex-1 min-w-0">
                        <div className="p-2 bg-primary/10 rounded-md">
                          <FileText className="h-4 w-4 text-primary flex-shrink-0" />
                        </div>
                        <div className="min-w-0 flex-1">
                        <p className="text-xs font-medium text-foreground truncate">{file.name}</p>
                        <p className="text-xs text-muted-foreground opacity-70">
                          {(file.size / 1024 / 1024).toFixed(1)} MB
                        </p>
                        </div>
                      </div>
                      <button
                        onClick={(e) => { e.stopPropagation(); removeFile(index); }}
                        className="h-8 w-8 flex items-center justify-center p-0 rounded-md hover:bg-destructive/10 hover:text-destructive transition-colors flex-shrink-0"
                        title="Remove"
                      >
                        <X className="h-4 w-4" />
                      </button>
                    </Card>
                  ))
                )}
              </div>
            </div>
          </div>
        </Card>
      </div>

      {/* Header Bar - Full Width */}
      <div className="absolute top-0 left-72 right-0 h-16 bg-background/95 backdrop-blur-lg border-b border-border/30 flex items-center justify-between px-6 rounded-b-3xl shadow-lg z-10">
        <div className="flex items-center gap-3">
          <div className="p-2 bg-primary/10 rounded-xl">
            <MessageSquare className="w-5 h-5 text-primary" />
          </div>
          <div>
            <h1 className="text-lg font-semibold text-foreground">Legal Document Chat</h1>
            <p className="text-xs text-muted-foreground">AI-powered legal analysis</p>
          </div>
        </div>
        <div className="flex items-center gap-2">
          <Button
            variant="outline"
            size="sm"
            onClick={() => setShowTemplates(!showTemplates)}
            className="h-9 px-3 rounded-xl hover:bg-primary/10 hover:text-primary transition-all"
            title="Document Templates"
          >
            <FileText className="w-4 h-4 mr-2" />
            Templates
          </Button>
          
          <Button
            variant="outline"
            size="sm"
            onClick={() => setShowAITools(!showAITools)}
            className="h-9 px-3 rounded-xl hover:bg-primary/10 hover:text-primary transition-all"
            title="Toggle AI Tools"
          >
            <Settings className="w-4 h-4 mr-2" />
            AI Tools
          </Button>
        </div>
      </div>

      {/* Main Content Area - Chat Interface */}
      <div className={`flex-1 flex h-full text-foreground relative pt-16 transition-all duration-300 ${showAITools ? 'mr-80' : ''}`}>
        <div className="flex-1 flex flex-col h-full">
          <Suspense fallback={<div className="flex items-center justify-center h-full">Loading chat...</div>}>
            <ChatInterface
              uploadedFile={selectedDocument}
              messages={messages}
              setMessages={setMessages}
              showRightPanel={false}
              onNewChat={handleNewChat}
              showAITools={showAITools}
            />
          </Suspense>
        </div>
      </div>

      {/* Template Selector Dropdown */}
      {showTemplates && (
        <>
          {/* Overlay */}
          <div 
            className="fixed inset-0 z-30"
            onClick={() => setShowTemplates(false)}
          />
          
          {/* Template Dropdown */}
          <div className="absolute top-16 right-4 z-40 min-w-80 max-w-md">
            <Card className="bg-background/95 backdrop-blur-lg border border-border shadow-2xl rounded-2xl overflow-hidden">
              <div className="p-4 border-b border-border">
                <div className="flex items-center justify-between mb-2">
                  <div className="flex items-center gap-2">
                    <FileText className="w-5 h-5 text-primary" />
                    <h3 className="text-lg font-semibold text-foreground">Document Templates</h3>
                  </div>
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={() => setShowTemplates(false)}
                    className="p-2 h-8 w-8"
                  >
                    <X className="w-4 h-4" />
                  </Button>
                </div>
                <p className="text-sm text-muted-foreground">
                  AI-powered document templates for legal drafting
                </p>
              </div>
              
              <div className="p-4 max-h-80 overflow-y-auto scrollbar-thin scrollbar-thumb-border scrollbar-track-transparent">
                <TemplateSelector />
              </div>
            </Card>
          </div>
        </>
      )}

      {/* AI Tools Slide-out Panel */}
      <AIToolsPanel 
        isOpen={showAITools}
        onClose={() => setShowAITools(false)}
        selectedDocument={selectedDocument}
        setMessages={setMessages}
        messages={messages}
      />
    </div>
  );
};

export default EnhancedDashboard;
