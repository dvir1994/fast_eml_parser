import pytesseract
from pdf2image import convert_from_bytes
import io
from PIL import Image


def image_ocr(image_path):
    # Open the image using Pillow
    img = Image.open(io.BytesIO(image_path))
    # Use pytesseract to do OCR on the image
    text = pytesseract.image_to_string(img, lang="eng", timeout=30)
    return text


def pdf_ocr(doc_path):
    images = convert_from_bytes(doc_path, fmt="png")
    total_text = ""

    for image in images:
        text = pytesseract.image_to_string(image, lang="eng", timeout=30)
        total_text += text

    return total_text
