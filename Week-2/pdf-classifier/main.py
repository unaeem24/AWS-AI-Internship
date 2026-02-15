import os
import config
import models
import utils

def main():
    # 1. Load AI Models
    classifier, qa_model = models.load_models()
    
    # 2. Check for files
    if not os.path.exists(config.TEST_FOLDER):
        print(f"Error: {config.TEST_FOLDER} not found.")
        return

    files = [os.path.join(config.TEST_FOLDER, f) for f in os.listdir(config.TEST_FOLDER) if f.lower().endswith('.pdf')]
    print(f"Found {len(files)} files. Starting processing...")

    for file_path in files:
        file_name = os.path.basename(file_path)
        print(f"\n--- Processing: {file_name} ---")

        # Step A: Extract Text
        raw_text = utils.extract_text_from_pdf(file_path)

        # Step B: Classify
        classification = classifier(raw_text[:2000], config.LABELS, multi_label=False)
        category = classification['labels'][0]
        print(f"   -> Category: {category}")

        # Step C: Extract Key-Value Pairs
        extracted_data = {}
        current_queries = config.QUESTIONS.get(category, ["What is the main topic?"])
        
        for q in current_queries:
            result = qa_model(question=q, context=raw_text[:3000])
            key = q.split()[-1].replace("?", "")
            extracted_data[key] = result['answer']

        # Step D: Save Results
        model_name = classifier.model.config._name_or_path.split('/')[-1]
        output_dir = os.path.join(config.DESIRED_OUTPUT_PATH, model_name)
        
        final_output = {
            "file": file_name,
            "category": category,
            "details": extracted_data
        }
        
        utils.save_json(final_output, output_dir, file_name)
        print(f"✅ Saved to: {output_dir}")

if __name__ == "__main__":
    main()