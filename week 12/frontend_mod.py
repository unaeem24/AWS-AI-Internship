import streamlit as st
import boto3
import time

# --- INITIAL SETUP ---
s3 = boto3.client('s3')
INPUT_BUCKET = "sight-proj-img-umair"
OUTPUT_BUCKET = "sight-proj-audio-umair"

st.set_page_config(page_title="Sight & Sound AI", page_icon="👁️", layout="centered")

# --- CUSTOM STYLING (CSS) ---
st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
        border-radius: 20px;
        background-color: #007bff;
        color: white;
    }
    .stAlert {
        border-radius: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- UI HEADER ---
st.title("👁️ Sight & Sound")
st.subheader("AI-Powered Accessibility Assistant")
st.markdown("---")

# --- SIDEBAR BRANDING ---
with st.sidebar:
    st.header("Project Info")
    st.info("Developed for the AWS AI Internship. This tool identifies living room objects for visually impaired users.")
    st.image("https://img.icons8.com/fluency/96/artificial-intelligence.png")

# --- MAIN LOGIC ---
uploaded_file = st.file_uploader("Upload a photo to hear your surroundings", type=["jpg", "png"])

if uploaded_file:
    # Show the user what they uploaded
    st.image(uploaded_file, caption="Image received successfully", use_container_width=True)
    
    # 1. Start the Backend Process
    file_name = uploaded_file.name
    
    # Use a Status container for a much better UX than a simple spinner
    with st.status("Initializing AI Pipeline...", expanded=True) as status:
        st.write("Uploading image to S3 secure storage...")
        s3.upload_fileobj(uploaded_file, INPUT_BUCKET, file_name)
        
        st.write("Triggering Lambda & AI Analysis (Bedrock + Polly)...")
        
        # 2. Polling for the Result
        audio_key = file_name.split('.')[0] + "_description.mp3"
        found = False
        
        # We try for 20 seconds instead of 15 just to be safe for Bedrock
        for i in range(20):
            try:
                s3.head_object(Bucket=OUTPUT_BUCKET, Key=audio_key)
                found = True
                break
            except:
                time.sleep(1)
        
        if found:
            status.update(label="Analysis Complete!", state="complete", expanded=False)
            
            # Generate the URL and Play
            url = s3.generate_presigned_url('get_object', 
                                          Params={'Bucket': OUTPUT_BUCKET, 'Key': audio_key})
            
            st.markdown("### 🔊 Voice Description")
            st.audio(url)
            
            # Accessibility: Autoplay hack for screen readers
            st.markdown(f'<audio autoplay src="{url}"></audio>', unsafe_allow_html=True)
            
            st.success("The scene has been described. Check the audio player above.")
            st.balloons()
        else:
            status.update(label="Analysis Timeout", state="error")
            st.error("The AI took too long to respond. Please check your AWS Lambda logs.")

else:
    st.write("Waiting for an image to analyze...")