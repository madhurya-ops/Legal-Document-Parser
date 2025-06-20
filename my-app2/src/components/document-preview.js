import React from 'react';
import { Button } from '../ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '../ui/card';
import { Badge } from '../ui/badge';
import { X, FileText, Download, Eye } from 'lucide-react';

export function DocumentPreview({ document, onClose }) {
  const formatFileSize = (bytes) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  const getFileType = (file) => {
    const extension = file.name.split('.').pop()?.toLowerCase();
    switch (extension) {
      case 'pdf':
        return { type: 'PDF Document', color: 'bg-red-100 text-red-800' };
      case 'doc':
      case 'docx':
        return { type: 'Word Document', color: 'bg-blue-100 text-blue-800' };
      case 'txt':
        return { type: 'Text Document', color: 'bg-gray-100 text-gray-800' };
      default:
        return { type: 'Document', color: 'bg-gray-100 text-gray-800' };
    }
  };

  const fileType = getFileType(document);

  return (
    <div className="h-full flex flex-col">
      <CardHeader className="border-b border-gray-200 dark:border-gray-700 pb-4">
        <div className="flex items-center justify-between">
          <CardTitle className="text-lg font-semibold text-gray-900 dark:text-gray-100 flex items-center gap-2">
            <FileText className="h-5 w-5" />
            Document Preview
          </CardTitle>
          <Button variant="ghost" size="sm" onClick={onClose}>
            <X className="h-4 w-4" />
          </Button>
        </div>
      </CardHeader>
      <CardContent className="flex-1 p-4 space-y-4">
        <div className="space-y-3">
          <div>
            <h3 className="font-medium text-gray-900 dark:text-gray-100 mb-1 truncate" title={document.name}>
              {document.name}
            </h3>
            <div className="flex items-center gap-2">
              <Badge className={fileType.color}>{fileType.type}</Badge>
              <span className="text-sm text-gray-500 dark:text-gray-400">{formatFileSize(document.size)}</span>
            </div>
          </div>
          <div className="grid grid-cols-2 gap-2">
            <Button variant="outline" size="sm" className="w-full">
              <Eye className="h-4 w-4 mr-2" />
              View
            </Button>
            <Button variant="outline" size="sm" className="w-full">
              <Download className="h-4 w-4 mr-2" />
              Download
            </Button>
          </div>
        </div>
        <div className="border-t border-gray-200 dark:border-gray-700 pt-4">
          <h4 className="font-medium text-gray-900 dark:text-gray-100 mb-2">Document Info</h4>
          <div className="space-y-2 text-sm">
            <div className="flex justify-between">
              <span className="text-gray-500 dark:text-gray-400">Type:</span>
              <span className="text-gray-900 dark:text-gray-100">{document.type || 'Unknown'}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-500 dark:text-gray-400">Size:</span>
              <span className="text-gray-900 dark:text-gray-100">{formatFileSize(document.size)}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-500 dark:text-gray-400">Modified:</span>
              <span className="text-gray-900 dark:text-gray-100">{new Date(document.lastModified).toLocaleDateString()}</span>
            </div>
          </div>
        </div>
        <Card className="bg-blue-50 dark:bg-blue-950 border-blue-200 dark:border-blue-800">
          <CardContent className="p-3">
            <div className="flex items-start gap-2">
              <FileText className="h-4 w-4 text-blue-600 dark:text-blue-400 mt-0.5 flex-shrink-0" />
              <div className="text-sm">
                <p className="font-medium text-blue-900 dark:text-blue-100 mb-1">Ready for Analysis</p>
                <p className="text-blue-700 dark:text-blue-300">
                  This document has been uploaded and is ready for AI analysis. Ask questions about its content in the chat.
                </p>
              </div>
            </div>
          </CardContent>
        </Card>
      </CardContent>
    </div>
  );
} 