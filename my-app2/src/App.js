import React, { useState, useMemo } from 'react';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Card } from './ui/card';
import { ScrollArea } from './ui/scroll-area';
import { Badge } from './ui/badge';
import { FileText, Scale, MessageSquare, Paperclip, X, Search, Moon, Sun } from 'lucide-react';
import { FileUpload } from './components/file-upload';
import { MessageList } from './components/message-list';
import { DocumentPreview } from './components/document-preview';

export default function App() {
  const [uploadedFiles, setUploadedFiles] = useState([]);
  const [selectedDocument, setSelectedDocument] = useState(null);
  const [searchQuery, setSearchQuery] = useState('');
  const [theme, setTheme] = useState('light');
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  // Filter documents based on search query
  const filteredDocuments = useMemo(() => {
    if (!searchQuery.trim()) return uploadedFiles;
    return uploadedFiles.filter((file) => file.name.toLowerCase().includes(searchQuery.toLowerCase()));
  }, [uploadedFiles, searchQuery]);

  const handleFileUpload = (files) => {
    setUploadedFiles((prev) => [...prev, ...files]);
  };

  const removeFile = (index) => {
    setUploadedFiles((prev) => prev.filter((_, i) => i !== index));
  };

  const onSubmit = async (e) => {
    e.preventDefault();
    if (!input.trim()) return;
    setIsLoading(true);
    // Simulate API call to backend
    try {
      // Replace with actual API call
      setMessages((prev) => [...prev, { id: Date.now(), role: 'user', content: input }]);
      // Simulate response
      setTimeout(() => {
        setMessages((prev) => [...prev, { id: Date.now() + 1, role: 'assistant', content: 'AI response...' }]);
        setIsLoading(false);
      }, 1000);
    } catch (err) {
      setIsLoading(false);
    }
    setInput('');
  };

  return (
    <div className={`flex h-screen bg-gray-50 ${theme === 'dark' ? 'dark bg-gray-900' : ''}`}>
      {/* Sidebar */}
      <div className="w-80 bg-white dark:bg-gray-800 border-r border-gray-200 dark:border-gray-700 flex flex-col">
        <div className="p-6 border-b border-gray-200 dark:border-gray-700">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center gap-3">
              <div className="p-2 bg-blue-600 rounded-lg">
                <Scale className="h-6 w-6 text-white" />
              </div>
              <div>
                <h1 className="text-xl font-semibold text-gray-900 dark:text-gray-100">LegalAI</h1>
                <p className="text-sm text-gray-500 dark:text-gray-400">Document Analysis</p>
              </div>
            </div>
            <Button
              variant="ghost"
              size="sm"
              onClick={() => setTheme(theme === 'dark' ? 'light' : 'dark')}
              className="h-8 w-8 p-0"
            >
              {theme === 'dark' ? <Sun className="h-4 w-4" /> : <Moon className="h-4 w-4" />}
            </Button>
          </div>
          <FileUpload onFileUpload={handleFileUpload} />
        </div>
        {/* Uploaded Files */}
        <div className="flex-1 p-4">
          <div className="space-y-3">
            <div className="flex items-center justify-between">
              <h3 className="text-sm font-medium text-gray-700 dark:text-gray-300">
                Documents ({uploadedFiles.length})
              </h3>
            </div>
            {/* Search Input */}
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
              <Input
                placeholder="Search documents..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="pl-9 h-8 text-sm"
              />
            </div>
          </div>
          <ScrollArea className="h-full mt-4">
            <div className="space-y-2">
              {filteredDocuments.length === 0 && searchQuery ? (
                <div className="text-center py-8">
                  <FileText className="h-8 w-8 text-gray-400 mx-auto mb-2" />
                  <p className="text-sm text-gray-500 dark:text-gray-400">No documents found</p>
                  <p className="text-xs text-gray-400 dark:text-gray-500">Try a different search term</p>
                </div>
              ) : (
                filteredDocuments.map((file, index) => (
                  <Card
                    key={index}
                    className="p-3 hover:bg-gray-50 dark:hover:bg-gray-800 cursor-pointer transition-colors"
                  >
                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-2 flex-1 min-w-0" onClick={() => setSelectedDocument(file)}>
                        <FileText className="h-4 w-4 text-blue-600 flex-shrink-0" />
                        <div className="min-w-0 flex-1">
                          <p className="text-sm font-medium text-gray-900 dark:text-gray-100 truncate">{file.name}</p>
                          <p className="text-xs text-gray-500 dark:text-gray-400">
                            {(file.size / 1024 / 1024).toFixed(2)} MB
                          </p>
                        </div>
                      </div>
                      <Button
                        variant="ghost"
                        size="sm"
                        onClick={() => removeFile(uploadedFiles.indexOf(file))}
                        className="h-6 w-6 p-0 hover:bg-red-100 dark:hover:bg-red-900"
                      >
                        <X className="h-3 w-3 text-red-500" />
                      </Button>
                    </div>
                  </Card>
                ))
              )}
            </div>
          </ScrollArea>
        </div>
      </div>
      {/* Main Chat Area */}
      <div className="flex-1 flex flex-col">
        {/* Header */}
        <div className="bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700 p-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <MessageSquare className="h-5 w-5 text-gray-600 dark:text-gray-400" />
              <h2 className="text-lg font-semibold text-gray-900 dark:text-gray-100">Legal Document Analysis</h2>
            </div>
            <div className="flex items-center gap-2">
              <Badge variant="secondary" className="bg-green-100 dark:bg-green-900 text-green-800 dark:text-green-200">
                AI Powered
              </Badge>
              <Badge variant="outline">{uploadedFiles.length} Documents</Badge>
            </div>
          </div>
        </div>
        {/* Messages */}
        <div className="flex-1 flex">
          <div className="flex-1 flex flex-col">
            <ScrollArea className="flex-1 p-4">
              {messages.length === 0 ? (
                <div className="flex items-center justify-center h-full">
                  <div className="text-center max-w-md">
                    <Scale className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                    <h3 className="text-lg font-medium text-gray-900 mb-2">Welcome to LegalAI Document Analyzer</h3>
                    <p className="text-gray-500 mb-6">
                      Upload your legal documents and ask questions to get AI-powered analysis, summaries, and insights.
                    </p>
                    <div className="grid grid-cols-1 gap-2 text-sm text-gray-600">
                      <div className="flex items-center gap-2">
                        <FileText className="h-4 w-4" />
                        <span>Contract analysis and review</span>
                      </div>
                      <div className="flex items-center gap-2">
                        <Scale className="h-4 w-4" />
                        <span>Legal compliance checking</span>
                      </div>
                      <div className="flex items-center gap-2">
                        <MessageSquare className="h-4 w-4" />
                        <span>Document summarization</span>
                      </div>
                    </div>
                  </div>
                </div>
              ) : (
                <MessageList messages={messages} isLoading={isLoading} />
              )}
            </ScrollArea>
            {/* Input Area */}
            <div className="border-t border-gray-200 dark:border-gray-700 p-4 bg-white dark:bg-gray-800">
              <form onSubmit={onSubmit} className="flex gap-2">
                <div className="flex-1 relative">
                  <Input
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    placeholder="Ask about your legal documents..."
                    className="pr-10"
                    disabled={isLoading}
                  />
                  {uploadedFiles.length > 0 && (
                    <div className="absolute right-3 top-1/2 transform -translate-y-1/2">
                      <Paperclip className="h-4 w-4 text-gray-400" />
                    </div>
                  )}
                </div>
                <Button type="submit" disabled={isLoading || !input.trim()}>
                  <span className="sr-only">Send</span>
                  <svg className="h-4 w-4" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" d="M22 2L11 13"></path><path strokeLinecap="round" strokeLinejoin="round" d="M22 2L15 22L11 13L2 9L22 2Z"></path></svg>
                </Button>
              </form>
              {uploadedFiles.length > 0 && (
                <div className="mt-2 flex flex-wrap gap-1">
                  {uploadedFiles.map((file, index) => (
                    <Badge key={index} variant="secondary" className="text-xs">
                      {file.name}
                    </Badge>
                  ))}
                </div>
              )}
            </div>
          </div>
          {/* Document Preview */}
          {selectedDocument && (
            <div className="w-96 border-l border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800">
              <DocumentPreview document={selectedDocument} onClose={() => setSelectedDocument(null)} />
            </div>
          )}
        </div>
      </div>
    </div>
  );
}