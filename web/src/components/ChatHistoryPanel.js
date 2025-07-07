import React from "react";
import { Card } from "./ui/card";
import { Button } from "./ui/button";
import { X, MessageSquare, Clock, Download, Plus, History, Trash2 } from "lucide-react";

const ChatHistoryPanel = ({ isOpen, onClose, messages = [], chatSessions = [], currentChatId, onChatSelect, onNewChat }) => {
  const formatTime = (timestamp) => {
    if (!timestamp) return '';
    const date = new Date(timestamp);
    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  const formatDate = (timestamp) => {
    if (!timestamp) return '';
    const date = new Date(timestamp);
    return date.toLocaleDateString();
  };

  // Group messages by date
  const groupedMessages = messages.reduce((groups, message) => {
    const date = formatDate(message.timestamp);
    if (!groups[date]) {
      groups[date] = [];
    }
    groups[date].push(message);
    return groups;
  }, {});

  // Create a mock session from current messages if no sessions exist
  const currentSession = messages.length > 0 ? {
    id: 'current',
    name: 'Current Chat',
    messages: messages,
    lastMessage: messages[messages.length - 1]?.content.substring(0, 50) + '...',
    timestamp: messages[messages.length - 1]?.timestamp || new Date()
  } : null;

  const displaySessions = currentSession ? [currentSession, ...chatSessions] : chatSessions;

  return (
    <>
      {/* Overlay */}
      {isOpen && (
        <div 
          className="fixed inset-0 bg-black/20 backdrop-blur-sm z-30"
          onClick={onClose}
        />
      )}
      
      {/* Slide-out Panel */}
      <div
        className={`fixed left-0 top-0 h-full w-80 bg-background/95 backdrop-blur-lg border-r border-border shadow-2xl z-40 transform transition-transform duration-300 ease-in-out ${
          isOpen ? 'translate-x-0' : '-translate-x-full'
        }`}
      >
        {/* Header */}
        <div className="p-4 border-b border-border">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center gap-2">
              <History className="w-5 h-5 text-primary" />
              <h2 className="text-lg font-semibold text-foreground">Chat Sessions</h2>
            </div>
            <Button
              variant="ghost"
              size="sm"
              onClick={onClose}
              className="p-2 h-8 w-8"
            >
              <X className="w-4 h-4" />
            </Button>
          </div>
          
          {/* New Chat Button */}
          <Button
            onClick={onNewChat}
            className="w-full justify-start gap-2 bg-primary/10 hover:bg-primary/20 text-primary border border-primary/20"
            size="sm"
          >
            <Plus className="w-4 h-4" />
            Start New Chat
          </Button>
        </div>

        {/* Content */}
        <div className="flex-1 overflow-y-auto p-4">
          {displaySessions.length === 0 ? (
            <div className="text-center py-8">
              <MessageSquare className="w-8 h-8 text-muted-foreground mx-auto mb-2" />
              <p className="text-sm text-muted-foreground">No chat sessions yet</p>
              <p className="text-xs text-muted-foreground mt-1">
                Start a new chat to begin
              </p>
            </div>
          ) : (
            <div className="space-y-2">
              {displaySessions.map((session) => (
                <Card
                  key={session.id}
                  className={`p-3 cursor-pointer transition-all hover:bg-muted/50 ${
                    currentChatId === session.id 
                      ? 'bg-primary/10 border-primary/50 shadow-sm' 
                      : 'hover:shadow-sm'
                  }`}
                  onClick={() => onChatSelect && onChatSelect(session.id)}
                >
                  <div className="flex items-start justify-between">
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center gap-2 mb-1">
                        <MessageSquare className="w-3 h-3 text-primary" />
                        <h4 className="text-sm font-medium text-foreground truncate">
                          {session.name}
                        </h4>
                      </div>
                      {session.lastMessage && (
                        <p className="text-xs text-muted-foreground line-clamp-2 mb-2">
                          {session.lastMessage}
                        </p>
                      )}
                      <div className="flex items-center gap-2 text-xs text-muted-foreground">
                        <Clock className="w-3 h-3" />
                        <span>{formatTime(session.timestamp)}</span>
                        <span>•</span>
                        <span>{session.messages?.length || 0} messages</span>
                      </div>
                    </div>
                  </div>
                </Card>
              ))}
            </div>
          )}
        </div>

        {/* Footer */}
        {displaySessions.length > 0 && (
          <div className="p-4 border-t border-border">
            <Button
              variant="outline"
              size="sm"
              className="w-full justify-start text-xs"
              onClick={() => {
                // Export functionality would go here
                console.log('Export chat sessions');
              }}
            >
              <Download className="w-4 h-4 mr-2" />
              Export All Chats
            </Button>
          </div>
        )}
      </div>
    </>
  );
};

export default ChatHistoryPanel;
