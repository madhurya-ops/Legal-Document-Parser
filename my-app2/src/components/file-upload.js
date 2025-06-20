import React, { useCallback, useState } from 'react';
import { useDropzone } from 'react-dropzone';
import { Card } from '../ui/card';
import { Upload } from 'lucide-react';
import { cn } from '../lib/utils';

export function FileUpload({ onFileUpload }) {
  const [uploadError, setUploadError] = useState(null);

  const onDrop = useCallback((acceptedFiles, rejectedFiles) => {
    setUploadError(null);
    if (rejectedFiles && rejectedFiles.length > 0) {
      setUploadError('Some files were rejected. Please upload PDF, DOC, or TXT files only.');
      return;
    }
    if (acceptedFiles.length > 0) {
      onFileUpload(acceptedFiles);
    }
  }, [onFileUpload]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf'],
      'application/msword': ['.doc'],
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx'],
      'text/plain': ['.txt'],
    },
    maxSize: 10 * 1024 * 1024, // 10MB
    multiple: true,
  });

  return (
    <div className="space-y-3">
      <Card
        {...getRootProps()}
        className={cn(
          'border-2 border-dashed cursor-pointer transition-colors',
          isDragActive
            ? 'border-blue-500 bg-blue-50 dark:bg-blue-950'
            : 'border-gray-300 dark:border-gray-600 hover:border-gray-400 dark:hover:border-gray-500'
        )}
      >
        <div className="p-6 text-center">
          <input {...getInputProps()} />
          <Upload className="h-8 w-8 text-gray-400 dark:text-gray-500 mx-auto mb-3" />
          <div className="space-y-2">
            <p className="text-sm font-medium text-gray-700 dark:text-gray-300">
              {isDragActive ? 'Drop files here' : 'Upload Documents'}
            </p>
            <p className="text-xs text-gray-500 dark:text-gray-400">Drag & drop or click to select</p>
            <p className="text-xs text-gray-400 dark:text-gray-500">PDF, DOC, DOCX, TXT (max 10MB)</p>
          </div>
        </div>
      </Card>
      {uploadError && (
        <div className="flex items-center gap-2 p-3 bg-red-50 dark:bg-red-950 border border-red-200 dark:border-red-800 rounded-lg">
          <span className="h-4 w-4 text-red-500 flex-shrink-0">!</span>
          <p className="text-sm text-red-700 dark:text-red-300">{uploadError}</p>
        </div>
      )}
    </div>
  );
} 