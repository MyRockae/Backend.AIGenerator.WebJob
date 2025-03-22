import PyPDF2
from docx import Document
from PIL import Image
import pytesseract
import os
import easyocr
import numpy as np

def readPdfFile(uploaded_file):
    file_content = ""
    reader = PyPDF2.PdfReader(uploaded_file)
    for page in reader.pages:
        text = page.extract_text()
        file_content += text if text else ""
    return file_content

def readWordFile(uploaded_file):
    doc = Document(uploaded_file)
    file_content = "\n".join([para.text for para in doc.paragraphs])
    return file_content

def readImageFile2(uploaded_file):
    image = Image.open(uploaded_file)
    file_content = pytesseract.image_to_string(image)
    return file_content


def readImageFile(uploaded_file):
    image = Image.open(uploaded_file)
    image_np = np.array(image)
    reader = easyocr.Reader(['en'])
    text_list = reader.readtext(image_np, detail=0)
    file_content = " ".join(text_list)
    return file_content


def extract_text_from_file(uploaded_file):
    filename = uploaded_file.name
    ext = os.path.splitext(filename)[1].lower()
    if ext == '.txt':
        return uploaded_file.read().decode('utf-8')
    elif ext == '.pdf':
        return readPdfFile(uploaded_file)
    elif ext == '.docx':
        return readWordFile(uploaded_file)
    elif ext in ['.png', '.jpg', '.jpeg']:
        return readImageFile(uploaded_file)
    else:
        raise ValueError("Unsupported file type.")
    

