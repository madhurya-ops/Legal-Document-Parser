import pypdf
import io
import logging
from typing import Optional

logger = logging.getLogger(__name__)

def extract_text_from_pdf(file_content: bytes) -> str:
    """
    Extract text content from PDF file bytes with enhanced error handling.
    
    Args:
        file_content: Raw bytes of the PDF file
        
    Returns:
        Extracted text content as string
    """
    if not file_content:
        logger.warning("No file content provided")
        return ""
    
    try:
        # Create a BytesIO object from the file content
        pdf_file = io.BytesIO(file_content)
        
        # Create a PDF reader object
        pdf_reader = pypdf.PdfReader(pdf_file)
        
        # Check if PDF is encrypted
        if pdf_reader.is_encrypted:
            logger.warning("PDF is encrypted, attempting to decrypt with empty password")
            try:
                pdf_reader.decrypt("")
            except Exception as decrypt_error:
                logger.error(f"Could not decrypt PDF: {decrypt_error}")
                return "This PDF is password protected. Please provide an unprotected version."
        
        # Extract text from pages with speed optimization
        text_content = []
        total_pages = len(pdf_reader.pages)
        max_pages_to_process = min(total_pages, 10)  # Limit pages for speed
        
        logger.info(f"Processing first {max_pages_to_process} pages of {total_pages} total pages")
        
        for page_num in range(max_pages_to_process):
            try:
                page = pdf_reader.pages[page_num]
                
                # Simple, fast extraction - just one method
                try:
                    page_text = page.extract_text()
                    if page_text and page_text.strip():
                        # Quick cleaning
                        cleaned_text = ' '.join(page_text.split())
                        if len(cleaned_text) > 50:  # Only add substantial content
                            text_content.append(cleaned_text)
                            logger.debug(f"Extracted {len(cleaned_text)} characters from page {page_num + 1}")
                            
                            # Stop if we have enough content for speed
                            if len('\n\n'.join(text_content)) > 5000:
                                logger.info("Sufficient content extracted, stopping for speed")
                                break
                except Exception as e:
                    logger.warning(f"Extraction failed for page {page_num + 1}: {e}")
                    continue
                    
            except Exception as page_error:
                logger.error(f"Error processing page {page_num + 1}: {page_error}")
                continue
        
        # Join all page contents
        if text_content:
            full_text = "\n\n".join(text_content)
            
            # Validate that we have actual text content, not just metadata
            if len(full_text.strip()) > 20 and not full_text.startswith("%PDF"):
                logger.info(f"Successfully extracted text from PDF: {len(full_text)} characters from {len(text_content)} pages")
                return full_text
            else:
                logger.warning("Extracted content appears to be metadata or insufficient text")
                return "Unable to extract meaningful text from this PDF. The document may contain only images, be scanned without OCR, or be in a format that doesn't support text extraction."
        else:
            logger.warning("No text could be extracted from any page of the PDF")
            return "Unable to extract text from this PDF. The document may contain only images or be in a format that doesn't support text extraction."
        
    except Exception as e:
        logger.error(f"Error extracting text from PDF: {e}")
        return f"Error reading PDF: {str(e)[:100]}. Please ensure the file is a valid PDF document."

def clean_extracted_text(text: str) -> str:
    """
    Clean and normalize extracted text from PDF.
    
    Args:
        text: Raw extracted text
        
    Returns:
        Cleaned text
    """
    if not text:
        return ""
    
    try:
        # Remove excessive whitespace
        text = ' '.join(text.split())
        
        # Remove common PDF artifacts
        text = text.replace('\x00', '')  # Remove null bytes
        text = text.replace('\ufffd', '')  # Remove replacement characters
        
        # Fix common spacing issues
        text = text.replace(' ,', ',')
        text = text.replace(' .', '.')
        text = text.replace(' ;', ';')
        text = text.replace(' :', ':')
        
        # Ensure sentences are properly spaced
        text = text.replace('.', '. ')
        text = text.replace('  ', ' ')  # Remove double spaces
        
        return text.strip()
        
    except Exception as e:
        logger.warning(f"Error cleaning text: {e}")
        return text

def is_pdf_file(filename: str) -> bool:
    """
    Check if the file is a PDF based on its extension.
    
    Args:
        filename: Name of the file
        
    Returns:
        True if it's a PDF file, False otherwise
    """
    return filename.lower().endswith('.pdf')
