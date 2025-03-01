import pytesseract
import os
from pdf2image import convert_from_bytes
from PIL import Image
from fastapi import UploadFile

def extract_text_from_file(file: UploadFile) -> str:
    """
    Extract text from images (JPEG, PNG) and PDFs using Tesseract OCR.
    """
    file_bytes = file.file.read()
    filename = file.filename.lower()

    if filename.endswith(".pdf"):
        images = convert_from_bytes(file_bytes)  # Convert PDF to images
        text = "\n".join([pytesseract.image_to_string(img) for img in images])
    
    elif filename.endswith((".png", ".jpg", ".jpeg", ".tiff", ".bmp", ".gif")):
        image = Image.open(file.file)
        text = pytesseract.image_to_string(image)
    
    else:
        raise ValueError("Unsupported file type. Please upload a PDF or image.")

    return text

def categorize_cashflow(text: str) -> dict:
    """
    Dummy categorization: Extracts amount and categorizes based on keywords.
    """
    amount_match = re.search(r"(\d+\.\d{2})", text)
    amount = float(amount_match.group(1)) if amount_match else 0.0
    text_lower = text.lower()
    category = "other"
    if "rent" in text_lower:
        category = "rent"
    elif "electricity" in text_lower or "elec" in text_lower:
        category = "electricity"
    elif "phone" in text_lower:
        category = "phone"
    elif "subscription" in text_lower:
        category = "subscriptions"

    # TODO: change to time
    return {"amount": amount, "category": category, "raw_text": text}

def categorize_official_document(text: str) -> dict:
    """
    Dummy categorization: Extracts amount and categorizes based on keywords.
    """
    amount_match = re.search(r"(\d+\.\d{2})", text)
    amount = float(amount_match.group(1)) if amount_match else 0.0
    category = "other"

    return {"category": category, "amount": amount}