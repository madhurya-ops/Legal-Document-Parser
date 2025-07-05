import React, { useRef, useEffect, useState } from "react";
import { Button } from "./ui/button";
import { Textarea } from "./ui/textarea";
import { Badge } from "./ui/badge";
import { Bot, User, FileText, Scale, Loader2, MessageSquare, Send } from "lucide-react";
import { sendQuery } from "../api";

export default function ChatInterface({ uploadedFile, messages, setMessages }) {
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const scrollAreaRef = useRef(null);
  const lastMessageRef = useRef(null);

  useEffect(() => {
    if (scrollAreaRef.current) {
      scrollAreaRef.current.scrollTop = scrollAreaRef.current.scrollHeight;
    }
  }, [messages]);

  useEffect(() => {
    if (lastMessageRef.current) {
      lastMessageRef.current.scrollIntoView({ behavior: 'smooth', block: 'end' });
    }
  }, [messages]);

  const handleSubmit = async (e) => {
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
      // Backend will use documents from vector store, no need to send file content
      const payload = { question: input };
      const answer = await sendQuery(payload);
      const assistantMessage = {
        id: (Date.now() + 1).toString(),
        type: "assistant",
        content: answer,
        timestamp: new Date(),
        sources: [],
      };
      setMessages((prev) => [...prev, assistantMessage]);
    } catch (error) {
      const errorMessage = {
        id: (Date.now() + 1).toString(),
        type: "assistant",
        content: "I apologize, but I encountered an error processing your request. Please try again.",
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="relative flex flex-col h-full w-full overflow-hidden bg-background bg-dots shadow-sm">
      {/* Chat area (scrollable) */}
      <div className="absolute inset-0 flex flex-col">
        <div className="flex-1 min-h-0 flex flex-col pb-[110px] bg-dots"> {/* Reserve space for input */}
          <div
            className="flex-1 min-h-0 p-4 sm:p-6 overflow-y-auto bg-dots pb-32"
            ref={scrollAreaRef}
            style={{ minHeight: 0 }}
          >
            <div className="space-y-4 sm:space-y-6">
              {messages.length === 0 ? (
                <div className="flex items-center justify-center h-full">
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
              ) : (
                messages.map((message, idx) => (
                  <div
                    key={message.id}
                    ref={idx === messages.length - 1 ? lastMessageRef : null}
                    className={`flex gap-3 sm:gap-4 ${message.type === "user" ? "justify-end" : "justify-start"} chat-message-animate`}
                  >
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
        {/* Input box (floating, translucent) */}
        <div className="absolute left-0 right-0 bottom-6 z-20 flex justify-center pointer-events-none bg-dots">
          <div className="backdrop-blur-md bg-background/90 bg-dots shadow-2xl rounded-2xl px-4 py-2 sm:px-6 sm:py-3 max-w-4xl w-[98%] pointer-events-auto border border-border">
            <form onSubmit={handleSubmit} className="flex gap-2 sm:gap-3 items-end">
              <Textarea
                id="chat-input"
                name="chat-input"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                placeholder="Ask about legal matters, case law, or your uploaded document..."
                className="flex-1 min-h-[36px] sm:min-h-[44px] resize-none bg-transparent border border-border text-foreground placeholder:text-muted-foreground focus:border-primary transition-colors duration-300 rounded-xl"
                onKeyDown={(e) => {
                  if (e.key === "Enter" && !e.shiftKey) {
                    e.preventDefault();
                    handleSubmit(e);
                  }
                }}
                disabled={isLoading}
              />
              <Button
                type="submit"
                disabled={!input.trim() || isLoading}
                className="bg-primary hover:bg-primary/90 text-primary-foreground h-[36px] sm:h-[44px] px-4 sm:px-6 transition-all duration-300 hover:scale-105 disabled:hover:scale-100 rounded-xl"
              >
                <Send className="w-4 h-4 sm:w-5 sm:h-5" />
              </Button>
            </form>
            <p className="text-xs text-muted-foreground mt-2 text-center sm:text-left">
              Press Enter to send • Shift+Enter for new line
            </p>
          </div>
        </div>
      </div>
    </div>
  );
} 
