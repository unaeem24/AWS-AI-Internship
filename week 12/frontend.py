import streamlit as st
import boto3
import time

s3 = boto3.client('s3')
INPUT_BUCKET = "sight-proj-img-umair"
OUTPUT_BUCKET = "sight-proj-audio-umair"

st.title("👁️ Sight & Sound Accessibility Bot")

uploaded_file = st.file_uploader("Upload a Living Room Photo", type=["jpg", "png"])

if uploaded_file:
    # 1. Upload to S3 (This automatically triggers your Lambda!)
    file_name = uploaded_file.name
    s3.upload_fileobj(uploaded_file, INPUT_BUCKET, file_name)
    st.info("Photo uploaded! AI is analyzing the scene...")

    # 2. Polling for the Result
    # We wait for the Lambda to finish and create the MP3
    audio_key = file_name.split('.')[0] + "_description.mp3"
    
    with st.spinner("Waiting for audio generation..."):
        for _ in range(15): # Try for 15 seconds
            try:
                # Check if the file exists yet
                s3.head_object(Bucket=OUTPUT_BUCKET, Key=audio_key)
                
                # If found, generate a temporary link to play it
                url = s3.generate_presigned_url('get_object', 
                                              Params={'Bucket': OUTPUT_BUCKET, 'Key': audio_key})
                st.audio(url)
                st.success("Analysis ready!")
                break
            except:
                time.sleep(1) # Wait 1 second before checking again