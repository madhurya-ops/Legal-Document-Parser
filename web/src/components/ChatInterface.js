import React, { useRef, useEffect, useState, useCallback, useMemo } from "react";
import { Button } from "./ui/button";
import { Textarea } from "./ui/textarea";
import { Badge } from "./ui/badge";
import { Bot, User, FileText, Scale, Loader2, MessageSquare, Send, Download, Plus, RotateCcw } from "lucide-react";
import { sendQuery, extractPdfText } from "../api";
import DocumentExporter from "./DocumentExporter";
import RightPanel from "./RightPanel";

function readFileAsText(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = () => resolve(reader.result);
    reader.onerror = reject;
    
    // Check if it's a PDF file
    if (file.type === 'application/pdf' || file.name.toLowerCase().endsWith('.pdf')) {
      // For PDFs, we'll extract text via backend API
      extractPDFText(file)
        .then(text => resolve(text))
        .catch(error => {
          console.error('PDF extraction failed:', error);
          resolve(''); // Return empty string if extraction fails
        });
    } else {
      // For other files, read as text
      reader.readAsText(file);
    }
  });
}

async function extractPDFText(file) {
  try {
    const data = await extractPdfText(file);
    return data.text || '';
  } catch (error) {
    console.error('Error extracting PDF text:', error);
    return '';
  }
}

const ChatInterface = React.memo(function ChatInterface({ uploadedFile, messages, setMessages, showRightPanel = true, onNewChat, showAITools = false }) {
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [fileText, setFileText] = useState("");
  const [showExporter, setShowExporter] = useState(false);
  const scrollAreaRef = useRef(null);
  const lastMessageRef = useRef(null);

  useEffect(() => {
    if (uploadedFile) {
      readFileAsText(uploadedFile).then(setFileText).catch(() => setFileText(""));
    } else {
      setFileText("");
    }
  }, [uploadedFile]);

  useEffect(() => {
    if (scrollAreaRef.current) {
      // Small delay to ensure DOM is updated
      const scrollToBottom = () => {
        scrollAreaRef.current.scrollTo({
          top: scrollAreaRef.current.scrollHeight,
          behavior: 'smooth'
        });
      };
      
      // Use requestAnimationFrame to ensure DOM is updated
      requestAnimationFrame(scrollToBottom);
    }
  }, [messages]);
  
  // Scroll when loading state changes to show loading indicator
  useEffect(() => {
    if (isLoading && scrollAreaRef.current) {
      setTimeout(() => {
        scrollAreaRef.current.scrollTo({
          top: scrollAreaRef.current.scrollHeight,
          behavior: 'smooth'
        });
      }, 100);
    }
  }, [isLoading]);

  const handleSubmit = useCallback(async (e) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;
    
    const userMessage = {
      id: Date.now().toString(),
      type: "user",
      content: input,
      timestamp: new Date(),
    };
    
    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setIsLoading(true);
    
    try {
      const payload = { question: input };
      if (fileText) {
        payload.file_content = fileText;
        payload.file_name = uploadedFile?.name;
      }
      
      console.log('Sending query to backend:', payload);
      const answer = await sendQuery(payload);
      console.log('Received response from backend:', answer);
      
      const assistantMessage = {
        id: (Date.now() + 1).toString(),
        type: "assistant",
        content: answer || "I received your message but couldn't generate a response. Please try again.",
        timestamp: new Date(),
        sources: [],
      };
      
      setMessages((prev) => [...prev, assistantMessage]);
    } catch (error) {
      console.error('Chat error:', error);
      const errorMessage = {
        id: (Date.now() + 1).toString(),
        type: "assistant",
        content: error.message || "I apologize, but I encountered an error processing your request. Please check your connection and try again.",
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  }, [input, isLoading, fileText, uploadedFile, setMessages]);
  
  const handleKeyDown = useCallback((e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  }, [handleSubmit]);
  
  const welcomeMessage = useMemo(() => (
    <div className="flex items-center justify-center min-h-[50vh]">
      <div className="text-center max-w-md mx-auto">
        <Scale className="h-12 w-12 text-muted-foreground mx-auto mb-4" />
        <h3 className="text-lg font-medium text-muted-foreground mb-2">Welcome to LegalDoc Document Analyzer</h3>
        <p className="text-muted-foreground mb-6">
          Upload your legal documents and ask questions to get AI-powered analysis, summaries, and insights.
        </p>
        <div className="flex flex-col items-center gap-2 text-sm text-muted-foreground">
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
  ), []);
  
  const loadingIndicator = useMemo(() => (
    <div className="flex gap-3 sm:gap-4 justify-start animate-fade-in">
      <div className="w-8 h-8 sm:w-10 sm:h-10 rounded-full bg-primary/10 flex items-center justify-center flex-shrink-0 transition-colors duration-300">
        <Bot className="w-4 h-4 sm:w-5 sm:h-5 text-primary" />
      </div>
      <div className="bg-background/90 rounded-2xl p-3 sm:p-4 border border-border transition-colors duration-300 backdrop-blur-sm">
        <div className="flex items-center gap-2">
          <Loader2 className="w-4 h-4 animate-spin text-primary" />
          <span className="text-sm text-muted-foreground">AI is thinking...</span>
        </div>
      </div>
    </div>
  ), []);

  return (
    <>
      {/* Chat messages area - with bottom padding for floating input */}
      <div className="flex-1 overflow-hidden">
        <div
          className="h-full p-4 sm:p-6 pb-44 overflow-y-auto"
          ref={scrollAreaRef}
          style={{ paddingBottom: '11rem' }}
        >
          <div className="space-y-4 sm:space-y-6">
              {messages.length === 0 ? (
                welcomeMessage
              ) : (
                messages.map((message, idx) => (
                  <div
                    key={message.id}
                    ref={idx === messages.length - 1 ? lastMessageRef : null}
                    className={`chat-message-animate ${
                      message.isToolResponse 
                        ? "w-full" // Tool responses take full width
                        : `flex gap-3 sm:gap-4 ${message.type === "user" ? "justify-end" : "justify-start"}`
                    }`}
                  >
                    {/* Tool Response Layout */}
                    {message.isToolResponse ? (
                      <div className="w-full mb-6">
                        <div className="bg-gradient-to-br from-primary/5 to-secondary/5 border border-primary/20 rounded-2xl p-6 shadow-lg">
                          <div className="flex items-center gap-3 mb-4">
                            <div className="p-2 bg-primary/10 rounded-xl">
                              <Bot className="w-5 h-5 text-primary" />
                            </div>
                            <div>
                              <h3 className="text-sm font-semibold text-foreground">AI Analysis Complete</h3>
                              <p className="text-xs text-muted-foreground">Tool: {message.toolUsed}</p>
                            </div>
                            <div className="ml-auto text-xs text-muted-foreground">
                              {message.timestamp.toLocaleTimeString()}
                            </div>
                          </div>
                          <div className="prose prose-sm max-w-none">
                            <div className="whitespace-pre-wrap text-sm leading-relaxed text-foreground">
                              {message.content}
                            </div>
                          </div>
                          {message.sources && message.sources.length > 0 && (
                            <div className="mt-4 pt-4 border-t border-border/30">
                              <div className="flex items-center gap-2 mb-2">
                                <Scale className="w-4 h-4 text-primary" />
                                <p className="text-xs font-medium text-muted-foreground">Analysis Sources:</p>
                              </div>
                              <div className="flex flex-wrap gap-2">
                                {message.sources.map((source, index) => (
                                  <Badge
                                    key={index}
                                    className="text-xs bg-primary/10 text-primary border-primary/20"
                                  >
                                    {source}
                                  </Badge>
                                ))}
                              </div>
                            </div>
                          )}
                        </div>
                      </div>
                    ) : (
                      /* Regular Chat Message Layout */
                      <>
                        {message.type === "assistant" && (
                          <div className="w-8 h-8 sm:w-10 sm:h-10 rounded-full bg-primary/10 flex items-center justify-center flex-shrink-0 transition-colors duration-300">
                            <Bot className="w-4 h-4 sm:w-5 sm:h-5 text-primary" />
                          </div>
                        )}
                        <div
                          className={"max-w-[85%] sm:max-w-[80%] rounded-2xl p-3 sm:p-4 shadow-sm transition-all duration-300 bg-background/90 text-foreground border border-border backdrop-blur-sm"}
                        >
                          <div className="whitespace-pre-wrap text-sm sm:text-base leading-relaxed">{message.content}</div>
                          {message.sources && message.sources.length > 0 && (
                            <div className="mt-3 pt-3 border-t border-border">
                              <div className="flex items-center gap-2 mb-2">
                                <Scale className="w-3 h-3 sm:w-4 sm:h-4 text-primary" />
                                <p className="text-xs font-medium text-muted-foreground">Relevant Cases:</p>
                              </div>
                              <div className="flex flex-wrap gap-1 sm:gap-2">
                                {message.sources.map((source, index) => (
                                  <Badge
                                    key={index}
                                    className="text-xs bg-background/80 text-foreground border-border"
                                  >
                                    {source}
                                  </Badge>
                                ))}
                              </div>
                            </div>
                          )}
                          <div className="text-xs opacity-60 mt-2">{message.timestamp.toLocaleTimeString()}</div>
                        </div>
                        {message.type === "user" && (
                          <div className="w-8 h-8 sm:w-10 sm:h-10 rounded-full bg-muted flex items-center justify-center flex-shrink-0 transition-colors duration-300">
                            <User className="w-4 h-4 sm:w-5 sm:h-5 text-muted-foreground" />
                          </div>
                        )}
                      </>
                    )}
                  </div>
                ))
              )}
              {isLoading && messages.length > 0 && (
                <div className="flex gap-3 sm:gap-4 justify-start animate-fade-in">
                  <div className="w-8 h-8 sm:w-10 sm:h-10 rounded-full bg-primary/10 flex items-center justify-center flex-shrink-0 transition-colors duration-300">
                    <Bot className="w-4 h-4 sm:w-5 sm:h-5 text-primary" />
                  </div>
                  <div className="bg-background/90 rounded-2xl p-3 sm:p-4 border border-border transition-colors duration-300 backdrop-blur-sm">
                    <div className="flex items-center gap-2">
                      <Loader2 className="w-4 h-4 animate-spin text-primary" />
                      <span className="text-sm text-muted-foreground">AI is thinking...</span>
                    </div>
                  </div>
                </div>
              )}
          </div>
        </div>
      </div>
      
      {/* Floating, fixed input box at bottom with curved edges - centered proportionally */}
      <div className={`fixed bottom-4 bg-background/95 backdrop-blur-md border border-border/50 rounded-2xl shadow-2xl p-4 z-50 transition-all duration-300 ${
        showAITools ? 'left-80 right-84' : 'left-80 right-4'
      }`} style={{
        left: '20rem',
        right: showAITools ? '21rem' : '1rem',
        maxWidth: 'none',
        width: 'auto'
      }}>
        <form onSubmit={handleSubmit} className="flex gap-3 items-center">
          <div className="flex-1 relative">
            <Textarea
              id="chat-input"
              name="chat-input"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Ask about legal matters, case law, or your uploaded document..."
              className="flex-1 min-h-[48px] max-h-32 resize-none bg-background/60 border border-border/40 text-foreground placeholder:text-muted-foreground focus:border-primary focus:ring-2 focus:ring-primary/20 transition-all duration-300 rounded-2xl px-4 py-3 text-sm leading-relaxed pr-12"
              onKeyDown={(e) => {
                if (e.key === "Enter" && !e.shiftKey) {
                  e.preventDefault();
                  handleSubmit(e);
                }
              }}
              disabled={isLoading}
            />
            {/* Character count indicator */}
            {input.length > 0 && (
              <div className="absolute bottom-2 right-3 text-xs text-muted-foreground">
                {input.length}
              </div>
            )}
          </div>
          
          {/* Action Buttons */}
          <div className="flex gap-2">
            {/* New Chat Button */}
            {onNewChat && (
              <Button
                type="button"
                variant="outline"
                onClick={onNewChat}
                className="h-[48px] px-4 transition-all duration-300 hover:scale-105 rounded-2xl border-border/40 hover:border-primary/50 hover:bg-primary/5"
                title="Start new chat"
              >
                <Plus className="w-5 h-5" />
              </Button>
            )}
            
            {/* Export Chat Button */}
            {messages.length > 0 && (
              <Button
                type="button"
                variant="outline"
                onClick={() => setShowExporter(true)}
                className="h-[48px] px-4 transition-all duration-300 hover:scale-105 rounded-2xl border-border/40 hover:border-primary/50 hover:bg-primary/5"
                title="Export chat"
              >
                <Download className="w-5 h-5" />
              </Button>
            )}
            
            {/* Send Button */}
            <Button
              type="submit"
              disabled={!input.trim() || isLoading}
              className="bg-gradient-to-r from-primary to-primary/80 hover:from-primary/90 hover:to-primary/70 text-primary-foreground h-[48px] px-6 transition-all duration-300 hover:scale-105 disabled:hover:scale-100 rounded-2xl shadow-lg font-medium"
            >
              {isLoading ? (
                <Loader2 className="w-5 h-5 animate-spin" />
              ) : (
                <Send className="w-5 h-5" />
              )}
            </Button>
          </div>
        </form>
        
        {/* Helper text */}
        <div className="flex items-center justify-between mt-3 pt-3 border-t border-border/20">
          <p className="text-xs text-muted-foreground">
            Press Enter to send • Shift+Enter for new line
          </p>
          {uploadedFile && (
            <div className="flex items-center gap-2 text-xs text-muted-foreground">
              <FileText className="w-3 h-3" />
              <span>Document ready for analysis</span>
            </div>
          )}
        </div>
      </div>
      
      {/* Document Exporter Modal */}
      {showExporter && (
        <DocumentExporter
          messages={messages}
          selectedDocument={uploadedFile}
          onClose={() => setShowExporter(false)}
        />
      )}
    </>
  );
});

export default ChatInterface;
