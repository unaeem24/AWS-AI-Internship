🎯**Overview**

This project provides a cost-effective, serverless pipeline for classifying and extracting data from digitally-native PDF documents. By combining Zero-Shot Classification and Span-based Question Answering, the system identifies document types (e.g., Invoices, CVs, Reports) and extracts key-value pairs without requiring manual training data.

🚀 **Key Features**

Intelligent Classification: Leverages DeBERTa-v3 for high-accuracy intent detection across 5 custom classes.

Layout-Agnostic Extraction: Uses a RoBERTa-based QA model to find data points (Total Amount, Candidate Name, etc.) within the text stream.

Cost Efficiency: Utilizes PyPDF for direct text stream parsing, bypassing expensive OCR services for digital files.

Modular Architecture: Separated into config, models, utils, and main modules for production-grade scalability.

🛠️ **Tech Stack**

Language: Python 3.10+

**AI Models:**

Classification: MoritzLaurer/DeBERTa-v3-large (1024-token limit)

Extraction: deepset/roberta-base-squad2 (SQuAD2 fine-tuned)

Libraries: transformers, pypdf, torch

Cloud (Future Target): AWS Lambda, S3, DynamoDB

📂 **Project Structure**

Plaintext

pdf-classifier/

├── config.py       # Centralized settings & label definitions

├── models.py       # Transformer pipeline initialization

├── utils.py        # PDF parsing and JSON serialization logic

├── main.py         # Primary execution script

└── test_samples/   # Input directory for PDF documents

⚙️ Setup & Installation

**Clone the Repository**

Bash

git clone https://github.com/unaeem24/AWS-AI-Internship.git
cd pdf-classifier
Set Up Virtual Environment

Bash

python -m venv myvenv
./myvenv/Scripts/activate  # Windows
Install Dependencies

Bash

pip install transformers pypdf torch
📊 Usage
Place your PDF files in the test_samples folder and run the main script:

Bash

python main.py
Output: Results are automatically saved in the Results/ directory, categorized by the model name.

📝 **Example Output (JSON)**
JSON

{
    "file": "invoice_77.pdf",
    "category": "Invoice",
    "details": {
        "amount": "$1,250.00",
        "number": "INV-2026-001"
    }
}

🛡️ **License**
Distributed under the MIT License. See LICENSE for more information.