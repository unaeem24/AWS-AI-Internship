import boto3

# 1. Connect to the "Comprehend" service (The AI brain for text)
ai_brain = boto3.client('comprehend', region_name='us-east-1')

# 2. These are the sentences we want to check
my_texts = [
    "I love learning new things at my internship!",
    "This error message is so annoying and frustrating.",
    "The book is on the table."
]

print("--- Starting Sentiment Analysis ---")

for text in my_texts:
    # 3. Ask the AI to detect the mood (Sentiment)
    result = ai_brain.detect_sentiment(Text=text, LanguageCode='en')
    
    # 4. Get the answer
    mood = result['Sentiment']
    
    print(f"Sentence: {text}")
    print(f"AI says the mood is: {mood}")
    print("-" * 30)
