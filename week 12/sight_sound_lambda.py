import boto3
import json
import os
import math 

def lambda_handler(event, context):
    # 1. INITIALIZE CLIENTS (The Remote Controls)
    s3 = boto3.client('s3')
    rek = boto3.client('rekognition')
    bedrock = boto3.client('bedrock-runtime')
    polly = boto3.client('polly')

    # 2. EXTRACT S3 DETAILS (The "Digital Envelope")
    # This grabs the bucket name and file name from the upload event
    try:
        bucket = event['Records'][0]['s3']['bucket']['name']
        image_key = event['Records'][0]['s3']['object']['key']
        
        # We define the name for our output audio file here
        # Example: 'photo.jpg' becomes 'photo_description.mp3'
        audio_key = image_key.split('.')[0] + "_description.mp3"
        output_bucket = "sight-proj-audio-umair" # Change this to your output bucket
    except Exception as e:
         print(f"Error extracting S3 info: {e}")
         print(f"Full event received: {json.dumps(event)}")
         raise 

    # 3. VISION PHASE (Amazon Rekognition)
    # We ask the "Eyes" to find objects and their locations (Bounding Boxes)
    print(f"Analyzing image: {image_key}")
    rek_response = rek.detect_labels(
        Image={'S3Object': {'Bucket': bucket, 'Name': image_key}},
        MaxLabels=10,
        MinConfidence=80
    )

    detected_items = []
    def get_clock_direction(box):
        # Calculate the center point of the object
        obj_x = box['Left'] + (box['Width'] / 2)
        obj_y = box['Top'] + (box['Height'] / 2)

        # Shift coordinates so center of image is (0,0)
        # Note: In images, Y increases downwards, so we flip it (-Y)
        dx = obj_x - 0.5
        dy = 0.5 - obj_y  

        # Calculate angle in degrees (0 degrees is 3 o'clock)
        angle_rad = math.atan2(dy, dx)
        angle_deg = math.degrees(angle_rad)

        # Convert angle to clock position (12, 1, 2, etc.)
        # Math: (90 - angle) / 30 aligns 90 degrees to 12 o'clock
        clock_val = round((90 - angle_deg) / 30)
        
        # Wrap around (e.g., 0 or 13 becomes 12)
        clock_val = clock_val % 12
        if clock_val == 0: clock_val = 12
        
        # Distance estimation (How close is it to the center?)
        distance = math.sqrt(dx**2 + dy**2)
        proximity = "directly in front" if distance < 0.15 else "in your surroundings"

        return f"at {clock_val} o'clock, {proximity}"

    # Use in your loop:
    for label in rek_response['Labels']:
        if label['Instances']:
            box = label['Instances'][0]['BoundingBox']
            direction = get_clock_direction(box)
            detected_items.append(f"{label['Name']} {direction}")

        # 5. BRAIN PHASE (Amazon Bedrock)
        # We send the list to Claude to turn into a helpful narrative
    
    labels_string = ", ".join(detected_items)
        


    system_prompt = """
        You are a professional Accessibility Assistant for the visually impaired. 
        Your goal is to provide a clear, concise, and spatially-aware description of the provided image to help a user navigate their environment safely.

        GUIDELINES:
        1. OVERVIEW: Start with a one-sentence summary of the environment (e.g., "You are in a busy kitchen" or "You are on a city sidewalk").
        2. NAVIGATION & SAFETY: Identify any obstacles directly in front of the user or on the floor (e.g., "There is a power cord on the floor 2 feet ahead").
        3. OBJECT PLACEMENT: Describe key objects using clock-face directions (e.g., "A wooden table is at your 2 o'clock") or relative positions (left, right, center).
        4. TEXT & SIGNS: If there is important text (like a "Restroom" sign or a "Caution" label), read it exactly as it appears.
        5. CONCISENESS: Keep the total description under 75 words. Avoid flowery or poetic language; be objective and factual.
        6. NO ASSUMPTIONS: Do not guess the user's intent. Only describe what is physically present in the image.

        FORMAT: 
        - Start immediately with the description. 
        - Do not say "In this image I see..." or "The photo shows..."
    """
    user_message = {
    "role": "user", 
    "content": [{"text": f"Detected objects in image are: {labels_string}"}]
    }

    # 2. Call the Bedrock Converse API
    response = bedrock.converse(
    modelId='us.anthropic.claude-3-5-haiku-20241022-v1:0', # Or Claude 3.5 Sonnet
    messages=[user_message],
    system=[{"text": system_prompt}], # This is where your custom logic lives
    inferenceConfig={
        "maxTokens": 200,
        "temperature": 0.4 # Lower temperature = more factual/less poetic
    }
    )
    
    # 6. EXTRACT THE TEXT
    # The Converse API puts the text in response['output']['message']['content']
    description_text = response['output']['message']['content'][0]['text']

    # 6. VOICE PHASE (Amazon Polly)
    # We turn the AI's words into a sound file
    print(f"Generating voice for: {description_text}")
    polly_response = polly.synthesize_speech(
        Text=description_text,
        OutputFormat='mp3',
        VoiceId='Joanna',
        Engine='neural' # Neural makes the voice sound very human
    )

    # 7. SAVE PHASE (S3 Output)
    # We save the MP3 back to S3 so the user can hear it
    s3.put_object(
        Bucket=output_bucket,
        Key=audio_key,
        Body=polly_response['AudioStream'].read(),
        ContentType='audio/mpeg'
    )

    return {
        'statusCode': 200,
        'body': json.dumps(f"Success! Audio saved to {audio_key}")
    }
