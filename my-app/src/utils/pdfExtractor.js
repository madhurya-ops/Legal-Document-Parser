// Document processing is now handled by the backend
// This file is kept for compatibility but processing is done server-side

export async function extractTextFromPDF(file) {
  // All PDF processing is now done on the backend using pypdf
  return `Document "${file.name}" will be processed by the backend server.

The backend will:
1. Extract text content from PDF pages using pypdf
2. Chunk the text for better processing
3. Create embeddings and add to vector store
4. Make content searchable for AI queries

File size: ${(file.size / 1024 / 1024).toFixed(2)}MB`;
}

export async function readFileContent(file) {
  const fileExtension = file.name.toLowerCase().split('.').pop();
  
  switch (fileExtension) {
    case 'pdf':
      return await extractTextFromPDF(file);
    
    case 'txt':
    case 'md':
      return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onload = () => resolve(reader.result);
        reader.onerror = reject;
        reader.readAsText(file);
      });
    
    case 'doc':
    case 'docx':
      // For now, return a message about DOC/DOCX files
      return `This is a Microsoft Word document (${file.name}). 

Word document processing requires specialized libraries. For now, please:
1. Save your document as a PDF or text file
2. Copy and paste the text content directly into the chat

The document is ${(file.size / 1024 / 1024).toFixed(2)}MB in size.`;
    
    default:
      return `Unsupported file type: ${fileExtension}. 

Supported formats:
- PDF files (.pdf)
- Text files (.txt)
- Markdown files (.md)

Please convert your document to one of these formats.`;
  }
}

