import os

# Paths
BASE_DIR = r"C:\Users\hp\OneDrive - Cloudelligent LLC\AWS-AI-Internship\Week-2\pdf-classifier"
TEST_FOLDER = os.path.join(BASE_DIR, "test_samples")
DESIRED_OUTPUT_PATH = os.path.join(BASE_DIR, "Results")

# Classification labels
LABELS = [
    "personal resume or curriculum vitae of a job candidate", 
    "financial invoice with billing details and total amount", 
    "academic scientific research paper or journal article", 
    "personal or professional email correspondence", 
    "business project status report or corporate documentation"
]
# Extraction questions
QUESTIONS = {
    "financial invoice with billing details and total amount": ["What is the total amount?", "What is the invoice number?"],
    "personal resume or curriculum vitae of a job candidate": ["What is the candidate's name?", "What is the highest degree?"],
    "business project status report or corporate documentation": ["What is the project name?", "Who is the Faculty Member?"],
    "academic scientific research paper or journal article": ["What is the title?", "Who is the lead author?"],
    "personal or professional email correspondence": ["Who is the sender?", "What is the subject?"]
}