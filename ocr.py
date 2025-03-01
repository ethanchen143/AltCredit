import re
from fastapi import UploadFile
# handling cashflow and official document
def extract_text_from_image(file: UploadFile) -> str:
    """
    Dummy OCR extraction.
    Replace with pytesseract or any real OCR lib in production.
    """
    content = file.file.read().decode("utf-8", errors="ignore")
    return content

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