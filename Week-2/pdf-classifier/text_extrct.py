from PyPDF2 import PdfReader

#import the model
import pytesseract

# This is the default path where the .exe installs it. 
# Update this if you chose a different folder!
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR'

def read_pdf(pdf_path):
    reader = PdfReader(pdf_path)

    for page_num, page in enumerate(reader.pages, start=1):
        text = page.extract_text()
        print(f"\n--- Page {page_num} ---\n")
        if text:
            print(text)
        else:
            print("[No extractable text found on this page]")

if __name__ == "__main__":
    pdf_file = r"C:\Users\hp\OneDrive - Cloudelligent LLC\Task Documentation\AI Intern Plan-details.pdf"   # replace with your PDF path
    read_pdf(pdf_file)
