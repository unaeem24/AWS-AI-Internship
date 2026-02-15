import os
import json
import torch
import pytesseract
from PIL import Image
from pdf2image import convert_from_path
from transformers import pipeline

# --- 1. CONFIGURATION & PATHS ---
# Update these to your verified paths from earlier!
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
os.environ['TESSDATA_PREFIX'] = r'C:\Program Files\Tesseract-OCR\tessdata'
POPPLER_PATH = r'C:\Popplar\poppler-25.12.0\Library\bin'

# --- 2. INITIALIZE AI MODELS ---
print("Initializing AI Models... please wait.")
# Zero-Shot Classifier (The Sorter)
classifier = pipeline("zero-shot-classification", 
                      model="MoritzLaurer/DeBERTa-v3-large-mnli-fever-anli-ling-wanli",
                      device=-1) # Change -1 to 0 if you have a GPU

# Document Question Answering (The Detail Extractor)
extractor = pipeline("document-question-answering", 
                     model="impira/layoutlm-document-qa")

def extract_details(image, doc_type):
    """Asks specific questions based on the identified document type."""
    data = {}
    questions = {
        "CV": {
            "name": "What is the name of the candidate?",
            "university": "What university did the person attend?",
            "degree": "What is the degree or major?"
        },
        "Invoice": {
            "invoice_no": "What is the invoice number?",
            "total": "What is the total amount to be paid?",
            "date": "What is the date of the invoice?"
        },
        "Scientific Document": {
            "title": "What is the title of the research paper?",
            "author": "Who is the lead author?"
        }
    }

    # Get the correct questions for the identified category
    query_set = questions.get(doc_type, {"summary": "What is the main topic of this document?"})

    print(f"   -> Extracting details for {doc_type}...")
    for key, question in query_set.items():
        result = extractor(image=image, question=question)
        data[key] = result[0]['answer'] if result else "Not found"
    
    return data
def process_single_pdf(pdf_path, classifier, extractor):
    """Full pipeline: PDF -> Image -> Text -> Category -> Extraction -> JSON."""
    try:
        print(f"\n--- Processing: {os.path.basename(pdf_path)} ---")
        
        # --- NEW: Set up Model-Specific Folder ---
        # Get the model name from the classifier (e.g., 'DeBERTa-v3-large')
        model_full_name = classifier.model.config._name_or_path
        # Clean the name to make it a valid folder name (removes '/' and special chars)
        model_folder_name = model_full_name.split('/')[-1]
        
        # Define the output directory path
        base_dir = os.path.dirname(pdf_path)
        output_dir = os.path.join(base_dir, model_folder_name)
        
        # Create the folder if it doesn't exist
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            print(f"Created output folder: {model_folder_name}")

        # Step A: Convert PDF to Image
        pages = convert_from_path(pdf_path, poppler_path=POPPLER_PATH, first_page=1, last_page=1)
        image = pages[0].convert("RGB")

        # Step B: Get Text via OCR
        raw_text = pytesseract.image_to_string(image)

        # Step C: Zero-Shot Classification
        candidate_labels = ["CV", "Invoice", "Scientific Document", "Email", "Project Report"]
        # Use the first 2000 characters for classification
        classification = classifier(raw_text[:2000], candidate_labels, multi_label=False)
        top_category = classification['labels'][0]
        confidence = classification['scores'][0]
        
        print(f"   -> Classified as: {top_category} ({confidence:.2f} confidence)")

        # Step D: Key-Value Extraction
        extracted_kv = extract_details(image, top_category)

        # Step E: Construct JSON Result
        final_output = {
            "metadata": {
                "source_file": os.path.basename(pdf_path),
                "category": top_category,
                "confidence_score": round(confidence, 4),
                "model_used": model_full_name
            },
            "extracted_data": extracted_kv
        }

        # --- STEP F: Save to the Specific Model Folder ---
        # Create filename based on original PDF name
        json_filename = os.path.basename(pdf_path).replace(".pdf", "_results.json")
        json_path = os.path.join(output_dir, json_filename)
        
        with open(json_path, "w") as f:
            json.dump(final_output, f, indent=4)
        
        print(f"✅ Success! Results saved in folder [{model_folder_name}] as: {json_filename}")

    except Exception as e:
        print(f"❌ Error processing {pdf_path}: {e}")

# --- MAIN EXECUTION BLOCK ---
if __name__ == "__main__":
    # Point to your test folder
    test_folder = r"C:\Users\hp\OneDrive - Cloudelligent LLC\AWS-AI-Internship\Week-2\pdf-classifier\test_samples"
    
    if not os.path.exists(test_folder):
        print("Error: Test folder path does not exist.")
    else:
        files = [os.path.join(test_folder, f) for f in os.listdir(test_folder) if f.lower().endswith('.pdf')]
        print(f"Found {len(files)} files. Starting automation...")
        
        for file in files:
            process_single_pdf(file, classifier, extractor)