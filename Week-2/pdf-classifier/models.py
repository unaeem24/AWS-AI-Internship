from transformers import pipeline

def load_models():
    print("Initializing models... this may take a moment.")
    classifier = pipeline("zero-shot-classification", 
                          model="MoritzLaurer/DeBERTa-v3-large-mnli-fever-anli-ling-wanli")
    
    qa_model = pipeline("question-answering", 
                        model="deepset/roberta-base-squad2")
    return classifier, qa_model