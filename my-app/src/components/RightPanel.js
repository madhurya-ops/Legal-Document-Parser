import React from 'react';
import { Button } from './ui/button';
import { Badge } from './ui/badge';
import { FileText, Scale, MessageSquare, Download } from 'lucide-react';

const RightPanel = ({ uploadedFile, messages, setInput, setShowExporter }) => {
  return (
    <div className="w-80 flex flex-col h-full bg-background/90 backdrop-blur-sm">
      {/* Panel Header */}
      <div className="px-4 py-4 border-b border-border bg-background/95">
        <h3 className="text-lg font-semibold text-foreground">Tools & Features</h3>
        <p className="text-sm text-muted-foreground">AI-powered legal assistance</p>
      </div>
      
      {/* Quick Actions */}
      <div className="p-4 space-y-3">
        <div className="space-y-2">
          <h4 className="text-sm font-medium text-foreground">Quick Actions</h4>
          <div className="grid grid-cols-1 gap-2">
            <Button
              variant="outline"
              size="sm"
              className="justify-start text-xs"
              onClick={() => setInput("Summarize this document")}
            >
              <FileText className="w-4 h-4 mr-2" />
              Summarize Document
            </Button>
            <Button
              variant="outline"
              size="sm"
              className="justify-start text-xs"
              onClick={() => setInput("What are the key legal risks in this document?")}
            >
              <Scale className="w-4 h-4 mr-2" />
              Identify Risks
            </Button>
            <Button
              variant="outline"
              size="sm"
              className="justify-start text-xs"
              onClick={() => setInput("Extract all important dates and deadlines")}
            >
              <MessageSquare className="w-4 h-4 mr-2" />
              Extract Dates
            </Button>
          </div>
        </div>
        
        {/* Document Info */}
        {uploadedFile && (
          <div className="border border-border rounded-lg p-3 bg-background/50">
            <h4 className="text-sm font-medium text-foreground mb-2">Current Document</h4>
            <div className="space-y-2">
              <div className="flex items-center gap-2">
                <FileText className="w-4 h-4 text-primary" />
                <span className="text-sm text-foreground truncate">{uploadedFile.name}</span>
              </div>
              <div className="text-xs text-muted-foreground">
                {(uploadedFile.size / 1024 / 1024).toFixed(2)} MB • {uploadedFile.type}
              </div>
              <Badge variant="secondary" className="text-xs">
                Ready for Analysis
              </Badge>
            </div>
          </div>
        )}
        
        {/* Export Options */}
        {messages.length > 0 && (
          <div className="space-y-2">
            <h4 className="text-sm font-medium text-foreground">Export Options</h4>
            <Button
              variant="outline"
              size="sm"
              onClick={() => setShowExporter(true)}
              className="w-full justify-start text-xs"
            >
              <Download className="w-4 h-4 mr-2" />
              Export Chat History
            </Button>
          </div>
        )}
        
        {/* Chat Statistics */}
        {messages.length > 0 && (
          <div className="border border-border rounded-lg p-3 bg-background/50">
            <h4 className="text-sm font-medium text-foreground mb-2">Session Stats</h4>
            <div className="space-y-1 text-xs text-muted-foreground">
              <div className="flex justify-between">
                <span>Total Messages:</span>
                <span className="text-foreground">{messages.length}</span>
              </div>
              <div className="flex justify-between">
                <span>Your Questions:</span>
                <span className="text-foreground">{messages.filter(m => m.type === 'user').length}</span>
              </div>
              <div className="flex justify-between">
                <span>AI Responses:</span>
                <span className="text-foreground">{messages.filter(m => m.type === 'assistant').length}</span>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default RightPanel;
