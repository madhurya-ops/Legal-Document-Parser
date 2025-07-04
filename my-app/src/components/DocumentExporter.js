import React, { useState } from 'react';
import { Button } from './ui/button';
import { Card } from './ui/card';
import { Download, FileText, Mail, Printer, X } from 'lucide-react';

const DocumentExporter = ({ messages, selectedDocument, onClose }) => {
  const [selectedFormat, setSelectedFormat] = useState('pdf');
  const [includeTimestamps, setIncludeTimestamps] = useState(true);
  const [includeSources, setIncludeSources] = useState(true);
  const [isExporting, setIsExporting] = useState(false);

  const exportFormats = [
    { id: 'pdf', name: 'PDF Document', icon: FileText },
    { id: 'docx', name: 'Word Document', icon: FileText },
    { id: 'txt', name: 'Plain Text', icon: FileText },
    { id: 'html', name: 'HTML Report', icon: FileText }
  ];

  const generateDocumentContent = () => {
    let content = '';
    
    // Header
    content += `LegalDoc Analysis Report\n`;
    content += `Generated on: ${new Date().toLocaleString()}\n`;
    content += `Document: ${selectedDocument?.name || 'Chat Session'}\n`;
    content += `\n${'='.repeat(50)}\n\n`;

    // Chat Messages
    messages.forEach((message, index) => {
      const timestamp = includeTimestamps ? ` [${message.timestamp.toLocaleTimeString()}]` : '';
      const role = message.type === 'user' ? 'USER' : 'AI ASSISTANT';
      
      content += `${role}${timestamp}:\n`;
      content += `${message.content}\n`;
      
      // Include sources if available and option is enabled
      if (includeSources && message.sources && message.sources.length > 0) {
        content += `\nSources: ${message.sources.join(', ')}\n`;
      }
      
      content += `\n${'-'.repeat(30)}\n\n`;
    });

    return content;
  };

  const downloadAsText = (content, filename) => {
    const blob = new Blob([content], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  const downloadAsHTML = (content, filename) => {
    const htmlContent = `
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>LegalDoc Analysis Report</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; line-height: 1.6; }
        .header { border-bottom: 2px solid #333; padding-bottom: 10px; margin-bottom: 20px; }
        .message { margin-bottom: 20px; padding: 15px; border-radius: 8px; }
        .user-message { background-color: #e3f2fd; border-left: 4px solid #2196f3; }
        .assistant-message { background-color: #f3e5f5; border-left: 4px solid #9c27b0; }
        .role { font-weight: bold; margin-bottom: 8px; }
        .timestamp { color: #666; font-size: 0.9em; }
        .sources { margin-top: 10px; font-style: italic; color: #555; }
        .content { white-space: pre-wrap; }
    </style>
</head>
<body>
    <div class="header">
        <h1>LegalDoc Analysis Report</h1>
        <p><strong>Generated:</strong> ${new Date().toLocaleString()}</p>
        <p><strong>Document:</strong> ${selectedDocument?.name || 'Chat Session'}</p>
    </div>
    
    <div class="messages">
        ${messages.map(message => `
            <div class="message ${message.type === 'user' ? 'user-message' : 'assistant-message'}">
                <div class="role">
                    ${message.type === 'user' ? 'USER' : 'AI ASSISTANT'}
                    ${includeTimestamps ? `<span class="timestamp"> - ${message.timestamp.toLocaleTimeString()}</span>` : ''}
                </div>
                <div class="content">${message.content}</div>
                ${includeSources && message.sources && message.sources.length > 0 ? 
                  `<div class="sources">Sources: ${message.sources.join(', ')}</div>` : ''
                }
            </div>
        `).join('')}
    </div>
</body>
</html>`;

    const blob = new Blob([htmlContent], { type: 'text/html' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  const handleExport = async () => {
    setIsExporting(true);
    
    try {
      const content = generateDocumentContent();
      const timestamp = new Date().toISOString().split('T')[0];
      const docName = selectedDocument?.name ? 
        selectedDocument.name.replace(/\.[^/.]+$/, '') : 
        'chat-session';
      const filename = `legaldoc-${docName}-${timestamp}`;

      switch (selectedFormat) {
        case 'txt':
          downloadAsText(content, `${filename}.txt`);
          break;
        case 'html':
          downloadAsHTML(content, `${filename}.html`);
          break;
        case 'pdf':
          // For PDF, we'll use the HTML content and let the browser handle it
          // In a real implementation, you'd use a library like jsPDF or html2pdf
          downloadAsHTML(content, `${filename}.html`);
          alert('PDF export: Please use your browser\'s print function to save as PDF from the downloaded HTML file.');
          break;
        case 'docx':
          // For DOCX, we'll use plain text for now
          // In a real implementation, you'd use a library like docx or mammoth
          downloadAsText(content, `${filename}.txt`);
          alert('DOCX export: Text file downloaded. For proper DOCX format, please copy the content to a Word document.');
          break;
        default:
          downloadAsText(content, `${filename}.txt`);
      }
    } catch (error) {
      console.error('Export error:', error);
      alert('Failed to export document. Please try again.');
    } finally {
      setIsExporting(false);
    }
  };

  const handlePrint = () => {
    const content = generateDocumentContent();
    const printWindow = window.open('', '_blank');
    printWindow.document.write(`
      <html>
        <head>
          <title>LegalDoc Analysis Report</title>
          <style>
            body { font-family: Arial, sans-serif; margin: 20px; line-height: 1.6; }
            .header { border-bottom: 2px solid #333; padding-bottom: 10px; margin-bottom: 20px; }
            .message { margin-bottom: 15px; page-break-inside: avoid; }
            .role { font-weight: bold; margin-bottom: 5px; }
            .content { white-space: pre-wrap; }
            @media print { body { margin: 0; } }
          </style>
        </head>
        <body>
          <div class="header">
            <h1>LegalDoc Analysis Report</h1>
            <p><strong>Generated:</strong> ${new Date().toLocaleString()}</p>
            <p><strong>Document:</strong> ${selectedDocument?.name || 'Chat Session'}</p>
          </div>
          <pre>${content}</pre>
        </body>
      </html>
    `);
    printWindow.document.close();
    printWindow.print();
  };

  const handleEmailShare = () => {
    const content = generateDocumentContent();
    const subject = encodeURIComponent(`LegalDoc Analysis Report - ${selectedDocument?.name || 'Chat Session'}`);
    const body = encodeURIComponent(content);
    const mailtoLink = `mailto:?subject=${subject}&body=${body}`;
    window.location.href = mailtoLink;
  };

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
      <Card className="w-full max-w-md p-6 bg-background">
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-lg font-semibold">Export Document</h2>
          <Button variant="ghost" size="sm" onClick={onClose}>
            <X className="w-4 h-4" />
          </Button>
        </div>

        <div className="space-y-6">
          {/* Format Selection */}
          <div>
            <label className="text-sm font-medium mb-3 block">Export Format</label>
            <div className="grid grid-cols-2 gap-2">
              {exportFormats.map((format) => (
                <button
                  key={format.id}
                  onClick={() => setSelectedFormat(format.id)}
                  className={`p-3 rounded-lg border text-left transition-colors ${
                    selectedFormat === format.id
                      ? 'border-primary bg-primary/10 text-primary'
                      : 'border-border hover:bg-muted'
                  }`}
                >
                  <format.icon className="w-4 h-4 mb-1" />
                  <div className="text-sm font-medium">{format.name}</div>
                </button>
              ))}
            </div>
          </div>

          {/* Options */}
          <div className="space-y-3">
            <label className="text-sm font-medium block">Export Options</label>
            
            <div className="flex items-center space-x-2">
              <input
                type="checkbox"
                id="timestamps"
                checked={includeTimestamps}
                onChange={(e) => setIncludeTimestamps(e.target.checked)}
                className="rounded border-border"
              />
              <label htmlFor="timestamps" className="text-sm">Include timestamps</label>
            </div>
            
            <div className="flex items-center space-x-2">
              <input
                type="checkbox"
                id="sources"
                checked={includeSources}
                onChange={(e) => setIncludeSources(e.target.checked)}
                className="rounded border-border"
              />
              <label htmlFor="sources" className="text-sm">Include source references</label>
            </div>
          </div>

          {/* Actions */}
          <div className="flex flex-col gap-2">
            <Button
              onClick={handleExport}
              disabled={isExporting || messages.length === 0}
              className="w-full"
            >
              <Download className="w-4 h-4 mr-2" />
              {isExporting ? 'Exporting...' : `Export as ${selectedFormat.toUpperCase()}`}
            </Button>
            
            <div className="flex gap-2">
              <Button
                variant="outline"
                onClick={handlePrint}
                disabled={messages.length === 0}
                className="flex-1"
              >
                <Printer className="w-4 h-4 mr-2" />
                Print
              </Button>
              
              <Button
                variant="outline"
                onClick={handleEmailShare}
                disabled={messages.length === 0}
                className="flex-1"
              >
                <Mail className="w-4 h-4 mr-2" />
                Email
              </Button>
            </div>
          </div>

          {messages.length === 0 && (
            <p className="text-sm text-muted-foreground text-center">
              No messages to export. Start a conversation first.
            </p>
          )}
        </div>
      </Card>
    </div>
  );
};

export default DocumentExporter;
