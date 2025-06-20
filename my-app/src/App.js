import React, { useState, useMemo } from "react";
import FileUpload from "./components/FileUpload";
import ChatInterface from "./components/ChatInterface";
import ThemeToggle from "./components/ThemeToggle";
import { Card } from "./components/ui/card";
import { Badge } from "./components/ui/badge";
import { ScrollArea } from "./components/ui/scroll-area";
import { Scale, FileText, MessageSquare, X, Search } from "lucide-react";
import "./App.css";

export default function App() {
  const [uploadedFiles, setUploadedFiles] = useState([]);
  const [selectedDocument, setSelectedDocument] = useState(null);
  const [messages, setMessages] = useState([]);
  const [searchQuery, setSearchQuery] = useState("");

  // Filter documents based on search query
  const filteredDocuments = useMemo(() => {
    if (!searchQuery.trim()) return uploadedFiles;
    return uploadedFiles.filter((file) => file.name.toLowerCase().includes(searchQuery.toLowerCase()));
  }, [uploadedFiles, searchQuery]);

  const handleFileUpload = (file) => {
    setUploadedFiles((prev) => [...prev, file]);
    setSelectedDocument(file); // auto-select latest
  };

  const removeFile = (index) => {
    setUploadedFiles((prev) => prev.filter((_, i) => i !== index));
    if (selectedDocument === uploadedFiles[index]) {
      setSelectedDocument(null);
    }
  };

  return (
    <div className="flex h-screen bg-slate-50 dark:bg-slate-900 transition-colors duration-300"> 
      {/* Sidebar */}
      <div className="w-72 flex flex-col h-200 m-4 rounded-2xl shadow-2xl backdrop-blur-md bg-white/80 dark:bg-slate-900/80 bg-dots border border-slate-200 dark:border-slate-700">
        {/* AppHeader */}
        <div className="p-4 flex items-center justify-between rounded-2xl shadow-2xl backdrop-blur-md bg-white/80 dark:bg-slate-900/80 bg-dots mb-2">
          <div className="flex items-center gap-3">
            <Scale className="w-7 h-7 text-blue-600 dark:text-blue-400" />
            <div>
              <span className="text-xl font-bold text-slate-900 dark:text-slate-100 tracking-tight">LegalAI</span>
              <div className="text-xs text-slate-500 dark:text-slate-400">Document Analysis</div>
            </div>
          </div>
          <ThemeToggle />
        </div>
        {/* UploadBox */}
        <div className="p-2">
          <FileUpload onFileUpload={handleFileUpload} selectedDocument={selectedDocument} boxSize="small" />
        </div>
        {/* SearchBar & Document List (Scrollable, sticky search) */}
        <ScrollArea className="flex-1 flex flex-col p-4">
          <div className="sticky top-0 z-10 bg-white dark:bg-slate-900 pb-2">
            <div className="relative mb-2">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-slate-400" />
              <input
                type="text"
                placeholder="Search documents..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="pl-9 pr-3 py-2 w-full rounded-md border border-slate-300 dark:border-slate-600 bg-slate-50 dark:bg-slate-800 text-sm text-slate-900 dark:text-slate-100 focus:outline-none focus:ring-2 focus:ring-blue-400"
              />
            </div>
            <div className="flex items-center justify-between mb-2">
              <h3 className="text-sm font-medium text-slate-700 dark:text-slate-300">
                Documents ({uploadedFiles.length})
              </h3>
            </div>
          </div>
          <div className="space-y-2">
            {filteredDocuments.length === 0 ? (
              <div className="text-center py-8">
                <FileText className="h-8 w-8 text-slate-400 mx-auto mb-2" />
                <p className="text-sm text-slate-500 dark:text-slate-400">No documents uploaded</p>
              </div>
            ) : (
              filteredDocuments.map((file, index) => (
                <Card
                  key={index}
                  className={`p-3 hover:bg-slate-50 dark:hover:bg-slate-800 cursor-pointer transition-colors flex items-center justify-between ${selectedDocument === file ? 'ring-2 ring-blue-500' : ''}`}
                  onClick={() => setSelectedDocument(file)}
                >
                  <div className="flex items-center gap-2 flex-1 min-w-0">
                    <FileText className="h-4 w-4 text-blue-600 flex-shrink-0" />
                    <div className="min-w-0 flex-1">
                      <p className="text-sm font-medium text-slate-900 dark:text-slate-100 truncate">{file.name}</p>
                      <p className="text-xs text-slate-500 dark:text-slate-400">
                        {(file.size / 1024 / 1024).toFixed(2)} MB
                      </p>
                    </div>
                  </div>
                  <button
                    onClick={e => { e.stopPropagation(); removeFile(index); }}
                    className="h-6 w-6 flex items-center justify-center p-0 rounded hover:bg-blue-100 dark:hover:bg-blue-900 transition-colors"
                    title="Remove"
                  >
                    <X className="h-4 w-4 text-blue-600 dark:text-blue-400 m-auto" />
                  </button>
                </Card>
              ))
            )}
          </div>
        </ScrollArea>
      </div>
      {/* Main Content Area */}
      <div className="flex-1 flex flex-col h-screen bg-slate-50 dark:bg-slate-900">
        {/* MainHeader */}
        <div className="p-4 border-b border-slate-200 dark:border-slate-700 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <MessageSquare className="h-5 w-5 text-slate-600 dark:text-slate-400" />
            <h2 className="text-xl font-semibold text-slate-900 dark:text-slate-100">Legal Document Analysis</h2>
          </div>
          <div className="flex items-center gap-2">
            <Badge className="bg-blue-100 dark:bg-blue-900 text-blue-800 dark:text-blue-200 rounded-full px-3 py-1 text-xs">AI Powered</Badge>
            <span className="text-xs text-slate-500 dark:text-slate-400">{uploadedFiles.length} Documents</span>
          </div>
        </div>
        {/* Main Content (Chat/Welcome) */}
        <div className="flex-1 flex flex-col justify-between">
          <div className="flex-1 overflow-y-auto">
            <div className="flex flex-col h-full">
              <div className="flex-1 flex flex-col">
                <div className="flex-1 flex flex-col">
                  <div className="flex-1 flex flex-col fade-in-chat">
                    <ChatInterface
                      uploadedFile={selectedDocument}
                      messages={messages}
                      setMessages={setMessages}
                    />
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}