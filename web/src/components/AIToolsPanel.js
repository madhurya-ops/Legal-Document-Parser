import React, { useState } from "react";
import { Card } from "./ui/card";
import { Button } from "./ui/button";
import { Badge } from "./ui/badge";
import { sendQuery, extractClauses, checkCompliance, searchPrecedents, extractPdfText } from "../api";
import { useAuth0 } from "@auth0/auth0-react";
import {
  FileText,
  Scale,
  AlertTriangle,
  Calendar,
  CheckCircle,
  Search,
  Clock,
  Zap,
  Lock,
  X,
  Settings
} from "lucide-react";

const AIToolsPanel = ({ isOpen, onClose, selectedDocument, messages, setMessages, onToolUsed }) => {
  const [loadingTool, setLoadingTool] = useState(null);
  const isDocumentUploaded = !!selectedDocument;
  const { getAccessTokenSilently } = useAuth0();

  const handleToolClick = async (toolName, query) => {
    if (!isDocumentUploaded) {
      // Show tooltip or notification that document is required
      return;
    }

    setLoadingTool(toolName);

    try {
      // Read file content if available
      let fileContent = '';
      if (selectedDocument) {
        try {
          fileContent = await readFileAsText(selectedDocument);
        } catch (error) {
          console.error('Error reading file:', error);
        }
      }

      let response;
      
      // Use specialized APIs based on tool type
      if (toolName === 'Clause Extractor') {
        console.log('Using clause extraction API');
        response = await extractClauses(fileContent, selectedDocument?.id, getAccessTokenSilently);
        response = formatClauseResponse(response);
      } else if (toolName === 'Compliance Checker') {
        console.log('Using compliance checking API');
        response = await checkCompliance(fileContent, 'india', selectedDocument?.id, getAccessTokenSilently);
        response = formatComplianceResponse(response);
      } else if (toolName === 'Legal Research') {
        console.log('Using precedent search API');
        response = await searchPrecedents(query, 'india', selectedDocument?.type, getAccessTokenSilently);
        response = formatPrecedentResponse(response);
      } else {
        // Use general query API for other tools
        const payload = {
          question: query,
          file_content: fileContent,
          file_name: selectedDocument?.name,
          tool_type: toolName.toLowerCase().replace(/\s+/g, '_')
        };
        console.log(`Sending ${toolName} request to backend:`, payload);
        response = await sendQuery(payload, getAccessTokenSilently);
        console.log(`Received ${toolName} response:`, response);
      }

      // Add AI response with tool indication
      const aiMessage = {
        id: Date.now().toString(),
        type: "assistant",
        content: response || `**${toolName} Analysis**\n\nAnalysis completed. Here are the key findings from your document.`,
        timestamp: new Date(),
        sources: [`${toolName} Analysis`],
        toolUsed: toolName,
        isToolResponse: true // Flag to identify tool responses
      };
      
      setMessages(prev => [...prev, aiMessage]);
      
      // Close the panel after tool usage
      if (onClose) {
        setTimeout(() => onClose(), 500);
      }
    } catch (error) {
      console.error(`${toolName} tool error:`, error);
      const errorMessage = {
        id: Date.now().toString(),
        type: "assistant",
        content: `**${toolName} Error**\n\nI encountered an error while analyzing your document with the ${toolName} tool. Please try again or check your connection.`,
        timestamp: new Date(),
        sources: [`${toolName} Error`],
        toolUsed: toolName,
        isToolResponse: true
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setLoadingTool(null);
    }
  };

  // Helper function to read file as text - same logic as ChatInterface
  const readFileAsText = (file) => {
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
  };
  
  // PDF text extraction function using the proper API
  const extractPDFText = async (file) => {
    try {
      const data = await extractPdfText(file);
      return data.text || '';
    } catch (error) {
      console.error('Error extracting PDF text:', error);
      return '';
    }
  };

  // Response formatting functions
  const formatClauseResponse = (response) => {
    if (!response || !response.clauses) return 'No clauses found in the document.';
    
    let formatted = '**Legal Clauses Extracted**\n\n';
    response.clauses.forEach((clause, index) => {
      formatted += `**${index + 1}. ${clause.type || 'Clause'}**\n${clause.content || clause.text || clause}\n\n`;
    });
    
    if (response.risk_assessment) {
      formatted += '**Risk Assessment:**\n';
      formatted += `- Risk Level: ${response.risk_assessment.level || 'Not specified'}\n`;
      formatted += `- Analysis: ${response.risk_assessment.analysis || 'Not provided'}\n\n`;
    }
    
    if (response.recommendations && response.recommendations.length > 0) {
      formatted += '**Recommendations:**\n';
      response.recommendations.forEach((rec, index) => {
        formatted += `${index + 1}. ${rec}\n`;
      });
    }
    
    return formatted;
  };

  const formatComplianceResponse = (response) => {
    if (!response) return 'No compliance analysis available.';
    
    let formatted = '**Compliance Analysis**\n\n';
    formatted += `**Status:** ${response.compliance_status || 'Unknown'}\n\n`;
    
    if (response.missing_clauses && response.missing_clauses.length > 0) {
      formatted += '**Missing Clauses:**\n';
      response.missing_clauses.forEach((clause, index) => {
        formatted += `${index + 1}. ${clause}\n`;
      });
      formatted += '\n';
    }
    
    if (response.regulatory_requirements && response.regulatory_requirements.length > 0) {
      formatted += '**Regulatory Requirements:**\n';
      response.regulatory_requirements.forEach((req, index) => {
        formatted += `${index + 1}. ${req.requirement || req}\n`;
      });
      formatted += '\n';
    }
    
    if (response.recommendations && response.recommendations.length > 0) {
      formatted += '**Recommendations:**\n';
      response.recommendations.forEach((rec, index) => {
        formatted += `${index + 1}. ${rec}\n`;
      });
    }
    
    if (response.confidence_score !== undefined) {
      formatted += `\n**Confidence Score:** ${(response.confidence_score * 100).toFixed(1)}%`;
    }
    
    return formatted;
  };

  const formatPrecedentResponse = (response) => {
    if (!response || !response.precedents || response.precedents.length === 0) {
      return 'No relevant legal precedents found.';
    }
    
    let formatted = '**Legal Precedents and Case Law**\n\n';
    
    response.precedents.forEach((precedent, index) => {
      formatted += `**${index + 1}. ${precedent.case_name || precedent.title || 'Case'}**\n`;
      if (precedent.court) formatted += `Court: ${precedent.court}\n`;
      if (precedent.year) formatted += `Year: ${precedent.year}\n`;
      if (precedent.summary) formatted += `Summary: ${precedent.summary}\n`;
      if (precedent.relevance) formatted += `Relevance: ${precedent.relevance}\n`;
      formatted += '\n';
    });
    
    if (response.citations && response.citations.length > 0) {
      formatted += '**Citations:**\n';
      response.citations.forEach((citation, index) => {
        formatted += `${index + 1}. ${citation}\n`;
      });
    }
    
    return formatted;
  };

  const aiTools = [
    {
      id: "summarize",
      name: "Document Summarizer",
      description: "Generate comprehensive document summaries",
      icon: FileText,
      query: "Please provide a comprehensive summary of this document, highlighting the key points and main themes.",
      color: "text-blue-500",
      bgColor: "bg-blue-500/10"
    },
    {
      id: "risks",
      name: "Risk Assessment",
      description: "Identify potential legal risks and concerns",
      icon: AlertTriangle,
      query: "What are the key legal risks and potential issues in this document?",
      color: "text-red-500",
      bgColor: "bg-red-500/10"
    },
    {
      id: "clauses",
      name: "Clause Extractor",
      description: "Extract and categorize important clauses",
      icon: Scale,
      query: "Extract and categorize all important legal clauses from this document.",
      color: "text-purple-500",
      bgColor: "bg-purple-500/10"
    },
    {
      id: "dates",
      name: "Date Extractor",
      description: "Find important dates and deadlines",
      icon: Calendar,
      query: "Extract all important dates, deadlines, and time-sensitive information from this document.",
      color: "text-green-500",
      bgColor: "bg-green-500/10"
    },
    {
      id: "compliance",
      name: "Compliance Checker",
      description: "Check regulatory compliance",
      icon: CheckCircle,
      query: "Analyze this document for compliance with relevant legal regulations and standards.",
      color: "text-indigo-500",
      bgColor: "bg-indigo-500/10"
    },
    {
      id: "precedents",
      name: "Legal Research",
      description: "Find relevant case law and precedents",
      icon: Search,
      query: "Find relevant legal precedents and case law related to this document.",
      color: "text-yellow-600",
      bgColor: "bg-yellow-500/10"
    }
  ];

  return (
    <div
      className={`fixed right-0 top-0 h-full w-80 bg-background/95 backdrop-blur-lg border-l border-border shadow-2xl z-30 transform transition-transform duration-300 ease-in-out flex flex-col ${
        isOpen ? 'translate-x-0' : 'translate-x-full'
      }`}
    >
        {/* Header */}
        <div className="p-4 border-b border-border">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center gap-2">
              <Settings className="w-5 h-5 text-primary" />
              <h2 className="text-lg font-semibold text-foreground">AI Tools</h2>
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
          
          <p className="text-sm text-muted-foreground mb-3">
            AI-powered legal analysis tools
          </p>
          
          {!isDocumentUploaded && (
            <div className="p-3 bg-yellow-500/10 border border-yellow-500/20 rounded-xl">
              <div className="flex items-center gap-2">
                <Lock className="w-4 h-4 text-yellow-600" />
                <p className="text-xs text-yellow-700 dark:text-yellow-400">
                  Upload a document to unlock AI tools
                </p>
              </div>
            </div>
          )}
        </div>

        {/* Current Document Info */}
        {selectedDocument && (
          <div className="p-4 border-b border-border">
            <h4 className="text-sm font-medium text-foreground mb-2">Active Document</h4>
            <Card className="p-3 bg-primary/5 border-primary/20 rounded-xl">
              <div className="flex items-center gap-2">
                <FileText className="w-4 h-4 text-primary" />
                <div className="flex-1 min-w-0">
                  <p className="text-sm font-medium text-foreground truncate">
                    {selectedDocument.name}
                  </p>
                  <div className="flex items-center gap-2 mt-1">
                    <Badge variant="secondary" className="text-xs">
                      Ready for Analysis
                    </Badge>
                    <span className="text-xs text-muted-foreground">
                      {(selectedDocument.size / 1024 / 1024).toFixed(1)} MB
                    </span>
                  </div>
                </div>
              </div>
            </Card>
          </div>
        )}

      {/* AI Tools Grid - Scrollable */}
      <div className="flex-1 overflow-y-auto scrollbar-thin scrollbar-thumb-border scrollbar-track-transparent p-4">
        <div className="space-y-3 pr-2">
          {aiTools.map((tool) => (
            <Card
              key={tool.id}
              className={`p-4 transition-all duration-200 cursor-pointer hover:shadow-md ${
                isDocumentUploaded && loadingTool !== tool.name
                  ? 'hover:scale-[1.02] hover:bg-muted/50' 
                  : 'opacity-60'
              } ${loadingTool === tool.name ? 'ring-2 ring-primary bg-primary/5' : ''}`}
              onClick={() => loadingTool === null && handleToolClick(tool.name, tool.query)}
            >
              <div className="flex items-start gap-3">
                <div className={`p-2 rounded-lg ${tool.bgColor} ${loadingTool === tool.name ? 'animate-pulse' : ''}`}>
                  {loadingTool === tool.name ? (
                    <Clock className="w-4 h-4 text-primary animate-spin" />
                  ) : (
                    <tool.icon className={`w-4 h-4 ${tool.color}`} />
                  )}
                </div>
                <div className="flex-1 min-w-0">
                  <h4 className="text-sm font-medium text-foreground mb-1">
                    {tool.name}
                  </h4>
                  <p className="text-xs text-muted-foreground leading-relaxed">
                    {tool.description}
                  </p>
                  
                  {isDocumentUploaded && (
                    <div className="flex items-center gap-1 mt-2">
                      {loadingTool === tool.name ? (
                        <>
                          <Clock className="w-3 h-3 text-primary animate-spin" />
                          <span className="text-xs text-primary font-medium">
                            Analyzing...
                          </span>
                        </>
                      ) : (
                        <>
                          <Zap className="w-3 h-3 text-primary" />
                          <span className="text-xs text-primary font-medium">
                            Click to analyze
                          </span>
                        </>
                      )}
                    </div>
                  )}
                </div>
              </div>
            </Card>
          ))}
        </div>
      </div>

        {/* Usage Stats */}
        {messages.length > 0 && (
          <div className="p-4 border-t border-border">
            <h4 className="text-sm font-medium text-foreground mb-2">Session Stats</h4>
            <Card className="p-3 bg-background/50 rounded-xl">
              <div className="space-y-2 text-xs">
                <div className="flex justify-between">
                  <span className="text-muted-foreground">Total Messages:</span>
                  <span className="text-foreground font-medium">{messages.length}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-muted-foreground">AI Analyses:</span>
                  <span className="text-foreground font-medium">
                    {messages.filter(m => m.type === 'assistant' && m.toolUsed).length}
                  </span>
                </div>
                <div className="flex justify-between">
                  <span className="text-muted-foreground">Tools Used:</span>
                  <span className="text-foreground font-medium">
                    {new Set(messages.filter(m => m.toolUsed).map(m => m.toolUsed)).size}
                  </span>
                </div>
              </div>
            </Card>
          </div>
        )}
    </div>
  );
};

export default AIToolsPanel;
