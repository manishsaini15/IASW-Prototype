import pytesseract
from PIL import Image
from pdf2image import convert_from_path
import os

def extract_text_from_document(file_path):
    ext = os.path.splitext(file_path)[1].lower()

    # PDF Support
    if ext == ".pdf":
        images = convert_from_path(file_path)
        full_text = ""

        for img in images:
            img = img.convert("RGB")   # FIX
            text = pytesseract.image_to_string(img)
            full_text += text + "\n"

        return full_text.strip()

    # Image Support
    img = Image.open(file_path)
    img = img.convert("RGB")   # FIX (very important)
    text = pytesseract.image_to_string(img)

    return text.strip()