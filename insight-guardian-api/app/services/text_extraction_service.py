# File: app/services/text_extraction_service.py
"""
Reusable service for extracting text from PDF and image files.
Supports PDF (using pdfplumber) and images (using pytesseract).
Can be extended for other formats or sources (S3, CDN, etc.).
"""

from typing import Union
from pathlib import Path
import pdfplumber
from PIL import Image
import pytesseract
import io

class TextExtractionService:
    @staticmethod
    def extract_text_from_pdf(file_bytes: bytes) -> str:
        """
        Extracts text from a PDF file given as bytes.
        """
        text = ""
        with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""
        return text

    @staticmethod
    def extract_text_from_image(file_bytes: bytes) -> str:
        """
        Extracts text from an image file given as bytes.
        """
        image = Image.open(io.BytesIO(file_bytes))
        text = pytesseract.image_to_string(image)
        return text

    @staticmethod
    def extract_text(file_bytes: bytes, file_type: str) -> str:
        """
        Unified method to extract text from supported file types.
        file_type: 'pdf', 'png', 'jpeg', etc.
        """
        if file_type.lower() == 'pdf':
            return TextExtractionService.extract_text_from_pdf(file_bytes)
        elif file_type.lower() in ['png', 'jpg', 'jpeg']:
            return TextExtractionService.extract_text_from_image(file_bytes)
        else:
            raise ValueError(f"Unsupported file type: {file_type}")
