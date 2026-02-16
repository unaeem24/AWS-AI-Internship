import os
import json
from pypdf import PdfReader
from transformers import pipeline

# --- 1. INITIALIZE MODELS ---
# We keep DeBERTa for its 1024-token limit and Zero-Shot smarts
classifier = pipeline("zero-shot-classification", 
                      model="MoritzLaurer/DeBERTa-v3-large-mnli-fever-anli-ling-wanli")

# For text-only extraction, we use a Question-Answering model
qa_model = pipeline("question-answering", model="deepset/roberta-base-squad2")

def process_with_pypdf(pdf_path):
    try:
        print(f"\n--- Processing: {os.path.basename(pdf_path)} ---")
        
        # Step A: Extract Text using PyPDF
        reader = PdfReader(pdf_path)
        raw_text = ""
        for page in reader.pages:
            raw_text += page.extract_text() + " "
        
        # Step B: Zero-Shot Classification
        labels = ["CV", "Invoice", "Scientific Document", "Email", "Project Report"]
        classification = classifier(raw_text[:2000], labels, multi_label=False)
        category = classification['labels'][0]
        
        print(f"   -> Category: {category}")

        # Step C: Extract Key-Value Pairs via Text-QA
        extracted_data = {}
        questions = {
            "Invoice": ["What is the total amount?", "What is the invoice number?"],
            "CV": ["What is the candidate's name?", "What is the highest degree?"],
            "Project Report": ["What is the project name?", "Who is the manager?"],
            "Scientific Document": ["What is the title?", "Who is the lead author?"],
            "Email": ["Who is the sender?", "What is the subject?"]
        }
        
        current_queries = questions.get(category, ["What is the main topic?"])
        
        for q in current_queries:
            # The QA model looks at the text and finds the specific answer
            result = qa_model(question=q, context=raw_text[:3000])
            key = q.split()[-1].replace("?", "")
            extracted_data[key] = result['answer']

        # Step D: Save to JSON in a Model-Named Folder
        model_name = classifier.model.config._name_or_path.split('/')[-1]
       # 1. Define your specific desired path
        desired_path = r"C:\Users\hp\OneDrive - Cloudelligent LLC\AWS-AI-Internship\Week-2\pdf-classifier\Results" 

        # 2. Update the join command
        output_dir = os.path.join(desired_path, model_name)
        
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        final_output = {
            "file": os.path.basename(pdf_path),
            "category": category,
            "details": extracted_data
        }

        json_path = os.path.join(output_dir, os.path.basename(pdf_path).replace(".pdf", ".json"))
        with open(json_path, "w") as f:
            json.dump(final_output, f, indent=4)
            
        print(f"✅ JSON saved to {model_name} folder.")

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
     
    test_folder = r"C:\Users\hp\OneDrive - Cloudelligent LLC\AWS-AI-Internship\Week-2\pdf-classifier\test_samples"
    
    if not os.path.exists(test_folder):
        print("Error: Test folder path does not exist.")
    else:
        files = [os.path.join(test_folder, f) for f in os.listdir(test_folder) if f.lower().endswith('.pdf')]
        print(f"Found {len(files)} files. Starting automation...")
        
        for file in files:
            process_with_pypdf(file)