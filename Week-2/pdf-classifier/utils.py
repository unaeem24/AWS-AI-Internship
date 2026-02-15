import os
import json
from pypdf import PdfReader

def extract_text_from_pdf(pdf_path):
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + " "
    return text

def save_json(data, output_dir, filename):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    save_path = os.path.join(output_dir, filename.replace(".pdf", ".json"))
    with open(save_path, "w") as f:
        json.dump(data, f, indent=4)