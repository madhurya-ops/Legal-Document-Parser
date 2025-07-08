import React, { useState, useEffect } from 'react';
import { Button } from './ui/button';
import { Badge } from './ui/badge';
import ChatInterface from './ChatInterface';
import ChatHistoryPanel from './ChatHistoryPanel';
import AIToolsPanel from './AIToolsPanel';
import ThemeToggle from './ThemeToggle';
import {
  Scale,
  LogOut,
  Settings,
  User,
  Search,
  X,
  Menu,
  History,
  Shield,
  Upload,
  FileText,
  ChevronRight,
  ChevronLeft,
  MessageSquare,
  Plus,
  Send,
  RotateCcw
} from 'lucide-react';
import { useAuth0 } from "@auth0/auth0-react";

const ModernDashboard = ({
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
  setShowHome,
  setUser,
  setShowAuth,
  setShowAbout,
  setShowAdminDashboard
}) => {
  const [showLeftPanel, setShowLeftPanel] = useState(true);
  const [showRightPanel, setShowRightPanel] = useState(true);
  const [showChatHistory, setShowChatHistory] = useState(false);
  const [chatSessions, setChatSessions] = useState([
    { id: 1, name: 'Contract Analysis', messages: [], lastMessage: 'What are the key terms in this contract?', timestamp: new Date() },
    { id: 2, name: 'Legal Research', messages: [], lastMessage: 'Help me understand property law', timestamp: new Date(Date.now() - 3600000) }
  ]);
  const [currentChatId, setCurrentChatId] = useState(1);
  const { logout } = useAuth0();

  const handleNewChat = () => {
    const newId = Math.max(...chatSessions.map(s => s.id)) + 1;
    const newSession = {
      id: newId,
      name: `New Chat ${newId}`,
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
  useEffect(() => {
    setChatSessions(prev => prev.map(session => 
      session.id === currentChatId 
        ? { ...session, messages, lastMessage: messages[messages.length - 1]?.content || '' }
        : session
    ));
  }, [messages, currentChatId]);

  return (
    <div className="min-h-screen bg-background bg-dots overflow-hidden">
      {/* Chat History Panel */}
      <ChatHistoryPanel 
        isOpen={showChatHistory}
        onClose={() => setShowChatHistory(false)}
        chatSessions={chatSessions}
        currentChatId={currentChatId}
        onChatSelect={handleChatSelect}
        onNewChat={handleNewChat}
      />

      {/* AI Tools Panel */}
      <AIToolsPanel 
        isOpen={showRightPanel}
        onClose={() => setShowRightPanel(false)}
        uploadedFile={selectedDocument}
        messages={messages}
        setMessages={setMessages}
        onToolUsed={(response) => {
          // Tool responses should not appear as chat bubbles
          // Instead, they appear as floating result cards
        }}
      />

      <div className="flex h-screen">
        {/* Left Panel - Floating */}
        <div className={`transition-all duration-300 ${showLeftPanel ? 'w-80' : 'w-16'} relative z-10`}>
          <div className="h-full p-4">
            <div className="bg-background/90 backdrop-blur-xl border border-border rounded-2xl shadow-2xl h-full flex flex-col">
              {/* Header */}
              <div className="p-6 border-b border-border/50">
                <div className="flex items-center justify-between mb-4">
                  <div className="flex items-center gap-3">
                    <div className="w-10 h-10 rounded-xl bg-primary/10 flex items-center justify-center">
                      <Scale className="w-6 h-6 text-primary" />
                    </div>
                    {showLeftPanel && (
                      <div>
                        <h1 className="text-lg font-bold text-foreground">LegalDoc</h1>
                        <p className="text-xs text-muted-foreground">Document Analysis</p>
                      </div>
                    )}
                  </div>
                  <div className="flex items-center gap-2">
                    {showLeftPanel && <ThemeToggle />}
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() => setShowLeftPanel(!showLeftPanel)}
                      className="p-2 h-8 w-8"
                    >
                      {showLeftPanel ? <ChevronLeft className="w-4 h-4" /> : <ChevronRight className="w-4 h-4" />}
                    </Button>
                  </div>
                </div>

                {/* User Info */}
                {showLeftPanel && (
                  <div className="flex items-center gap-3 p-3 bg-muted/30 rounded-xl">
                    <div className="w-10 h-10 rounded-full bg-primary/20 flex items-center justify-center">
                      <span className="text-sm font-medium text-primary">
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
                    <div className="flex items-center gap-1">
                      {/* Admin Badge */}
                      {(user?.role === 'admin' || ['admin1', 'admin2', 'admin3', 'admin4'].includes(user?.username)) && (
                        <Button
                          variant="ghost"
                          size="sm"
                          onClick={() => setShowAdminDashboard(true)}
                          className="p-1 h-6 w-6"
                          title="Admin Dashboard"
                        >
                          <Shield className="w-3 h-3" />
                        </Button>
                      )}
                      <Button
                        variant="ghost"
                        size="sm"
                        onClick={() => logout({ logoutParams: { returnTo: window.location.origin } })}
                        className="p-1 h-6 w-6 text-destructive hover:text-destructive"
                        title="Logout"
                      >
                        <LogOut className="w-3 h-3" />
                      </Button>
                    </div>
                  </div>
                )}
              </div>

              {showLeftPanel && (
                <>
                  {/* Upload Section */}
                  <div className="p-6 border-b border-border/50">
                    <div className="bg-muted/20 border-2 border-dashed border-border rounded-xl p-6 text-center hover:bg-muted/30 transition-colors cursor-pointer">
                      <Upload className="w-8 h-8 text-muted-foreground mx-auto mb-3" />
                      <h3 className="text-sm font-medium text-foreground mb-1">Upload Legal Document</h3>
                      <p className="text-xs text-muted-foreground mb-3">
                        Drag and drop your file here, or click anywhere in this box
                      </p>
                      <p className="text-xs text-muted-foreground">
                        Supports PDF, DOC, DOCX, TXT files
                      </p>
                    </div>
                  </div>

                  {/* Documents Section */}
                  <div className="flex-1 p-6 overflow-hidden">
                    <div className="flex items-center justify-between mb-4">
                      <h3 className="text-sm font-medium text-foreground">Documents ({uploadedFiles.length})</h3>
                    </div>
                    
                    {/* Search */}
                    <div className="relative mb-4">
                      <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground" />
                      <input
                        type="text"
                        placeholder="Search documents..."
                        value={searchQuery}
                        onChange={(e) => setSearchQuery(e.target.value)}
                        className="pl-9 pr-3 py-2 w-full rounded-xl border border-border bg-background/50 text-sm text-foreground focus:outline-none focus:ring-2 focus:ring-primary placeholder:text-muted-foreground"
                      />
                    </div>

                    {/* Document List */}
                    <div className="space-y-2 overflow-y-auto">
                      {filteredDocuments.length === 0 ? (
                        <div className="text-center py-8">
                          <FileText className="h-12 w-12 text-muted-foreground mx-auto mb-3 opacity-50" />
                          <p className="text-sm text-muted-foreground">No documents uploaded</p>
                        </div>
                      ) : (
                        filteredDocuments.map((file, index) => (
                          <div
                            key={index}
                            className={`p-3 rounded-xl border cursor-pointer transition-all hover:bg-muted/20 ${
                              selectedDocument === file
                                ? 'bg-primary/10 border-primary/50'
                                : 'bg-background/30 border-border/50'
                            }`}
                            onClick={() => setSelectedDocument(file)}
                          >
                            <div className="flex items-center gap-3">
                              <FileText className="w-4 h-4 text-primary" />
                              <div className="flex-1 min-w-0">
                                <p className="text-sm font-medium text-foreground truncate">
                                  {file.name}
                                </p>
                                <p className="text-xs text-muted-foreground">
                                  {(file.size / 1024 / 1024).toFixed(2)} MB
                                </p>
                              </div>
                              <Button
                                variant="ghost"
                                size="sm"
                                onClick={(e) => {
                                  e.stopPropagation();
                                  removeFile(index);
                                }}
                                className="p-1 h-6 w-6 text-muted-foreground hover:text-destructive"
                              >
                                <X className="w-3 h-3" />
                              </Button>
                            </div>
                          </div>
                        ))
                      )}
                    </div>
                  </div>
                </>
              )}
            </div>
          </div>
        </div>

        {/* Main Content - Floating */}
        <div className="flex-1 relative">
          <div className="h-full p-4">
            {/* Header Bar */}
            <div className="bg-background/90 backdrop-blur-xl border border-border rounded-2xl shadow-lg mb-4 p-4">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-4">
                  <MessageSquare className="w-5 h-5 text-primary" />
                  <h2 className="text-lg font-medium text-foreground">
                    {chatSessions.find(s => s.id === currentChatId)?.name || 'Legal Document Analysis'}
                  </h2>
                  <Badge variant="secondary" className="text-xs">
                    AI Powered
                  </Badge>
                  <Badge variant="outline" className="text-xs">
                    {uploadedFiles.length} Documents
                  </Badge>
                </div>
                <div className="flex items-center gap-2">
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={() => setShowChatHistory(!showChatHistory)}
                    className="flex items-center gap-2"
                  >
                    <History className="w-4 h-4" />
                    Chat History
                  </Button>
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={() => setShowRightPanel(!showRightPanel)}
                    className="flex items-center gap-2"
                  >
                    <Settings className="w-4 h-4" />
                    AI Tools
                  </Button>
                </div>
              </div>
            </div>

            {/* Chat Area */}
            <div className="bg-background/90 backdrop-blur-xl border border-border rounded-2xl shadow-lg h-[calc(100vh-200px)] flex flex-col overflow-hidden">
              <ChatInterface
                uploadedFile={selectedDocument}
                messages={messages}
                setMessages={setMessages}
                showRightPanel={false}
                onNewChat={handleNewChat}
              />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ModernDashboard;
