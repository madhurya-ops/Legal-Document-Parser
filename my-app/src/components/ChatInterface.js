import React, { useRef, useEffect, useState } from "react";
import { Button } from "./ui/button";
import { Textarea } from "./ui/textarea";
import { Badge } from "./ui/badge";
import { Bot, User, FileText, Scale, Loader2, MessageSquare, Send } from "lucide-react";
import { sendQuery } from "../api";

function readFileAsText(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = () => resolve(reader.result);
    reader.onerror = reject;
    reader.readAsText(file);
  });
}

export default function ChatInterface({ uploadedFile, messages, setMessages }) {
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [fileText, setFileText] = useState("");
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
      const payload = { question: input };
      if (fileText) payload.file_content = fileText;
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
    <div className="relative flex flex-col h-full w-full overflow-hidden bg-slate-50 dark:bg-slate-900 shadow-sm">
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
                    <Scale className="h-12 w-12 text-slate-400 mx-auto mb-4" />
                    <h3 className="text-lg font-medium text-slate-600 dark:text-slate-400 mb-2">Welcome to LegalAI Document Analyzer</h3>
                    <p className="text-slate-600 dark:text-slate-400 mb-6">
                      Upload your legal documents and ask questions to get AI-powered analysis, summaries, and insights.
                    </p>
                    <div className="flex flex-col items-center gap-2 text-sm text-slate-600">
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
                    <div className="w-8 h-8 sm:w-10 sm:h-10 rounded-full bg-blue-100 dark:bg-blue-900/30 flex items-center justify-center flex-shrink-0 transition-colors duration-300">
                      <Bot className="w-4 h-4 sm:w-5 sm:h-5 text-blue-600 dark:text-blue-400" />
                    </div>
                  )}
                  <div
                      className={"max-w-[85%] sm:max-w-[80%] rounded-2xl p-3 sm:p-4 shadow-sm transition-all duration-300 bg-slate-100 dark:bg-slate-700 text-slate-900 dark:text-slate-100 border border-slate-200 dark:border-slate-600"}
                  >
                    <div className="whitespace-pre-wrap text-sm sm:text-base leading-relaxed">{message.content}</div>
                    {message.sources && message.sources.length > 0 && (
                      <div className="mt-3 pt-3 border-t border-slate-200 dark:border-slate-600">
                        <div className="flex items-center gap-2 mb-2">
                          <Scale className="w-3 h-3 sm:w-4 sm:h-4 text-blue-500" />
                          <p className="text-xs font-medium text-slate-600 dark:text-slate-400">Relevant Cases:</p>
                        </div>
                        <div className="flex flex-wrap gap-1 sm:gap-2">
                          {message.sources.map((source, index) => (
                            <Badge
                              key={index}
                              className="text-xs bg-white dark:bg-slate-800 text-slate-700 dark:text-slate-300 border-slate-300 dark:border-slate-600"
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
                    <div className="w-8 h-8 sm:w-10 sm:h-10 rounded-full bg-slate-200 dark:bg-slate-700 flex items-center justify-center flex-shrink-0 transition-colors duration-300">
                      <User className="w-4 h-4 sm:w-5 sm:h-5 text-slate-600 dark:text-slate-400" />
                    </div>
                  )}
                </div>
                ))
              )}
              {isLoading && messages.length > 0 && (
                <div className="flex gap-3 sm:gap-4 justify-start animate-fade-in">
                  <div className="w-8 h-8 sm:w-10 sm:h-10 rounded-full bg-blue-100 dark:bg-blue-900/30 flex items-center justify-center flex-shrink-0 transition-colors duration-300">
                    <Bot className="w-4 h-4 sm:w-5 sm:h-5 text-blue-600 dark:text-blue-400" />
                  </div>
                  <div className="bg-slate-100 dark:bg-slate-700 rounded-2xl p-3 sm:p-4 border border-slate-200 dark:border-slate-600 transition-colors duration-300">
                    <div className="flex items-center gap-2">
                      <Loader2 className="w-4 h-4 animate-spin text-blue-500" />
                      <span className="text-sm text-slate-600 dark:text-slate-400">AI is thinking...</span>
                    </div>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
        {/* Input box (floating, translucent) */}
        <div className="absolute left-0 right-0 bottom-6 z-20 flex justify-center pointer-events-none bg-dots">
          <div className="backdrop-blur-md bg-white/80 dark:bg-slate-800/80 bg-dots shadow-2xl rounded-2xl px-4 py-2 sm:px-6 sm:py-3 max-w-4xl w-[98%] pointer-events-auto border border-slate-200 dark:border-slate-700">
            <form onSubmit={handleSubmit} className="flex gap-2 sm:gap-3 items-end">
            <Textarea
                id="chat-input"
                name="chat-input"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Ask about legal matters, case law, or your uploaded document..."
                className="flex-1 min-h-[36px] sm:min-h-[44px] resize-none bg-transparent border border-slate-300 dark:border-slate-600 text-slate-900 dark:text-slate-100 placeholder:text-slate-500 dark:placeholder:text-slate-400 focus:border-blue-400 dark:focus:border-blue-500 transition-colors duration-300 rounded-xl"
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
                className="bg-blue-600 hover:bg-blue-700 text-white h-[36px] sm:h-[44px] px-4 sm:px-6 transition-all duration-300 hover:scale-105 disabled:hover:scale-100 rounded-xl"
            >
              <Send className="w-4 h-4 sm:w-5 sm:h-5" />
            </Button>
          </form>
          <p className="text-xs text-slate-500 dark:text-slate-400 mt-2 text-center sm:text-left">
            Press Enter to send • Shift+Enter for new line
          </p>
        </div>
        </div>
      </div>
    </div>
  );
} 