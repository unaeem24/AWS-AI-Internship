import boto3

# Initialize the Rekognition client for the us-east-1 region
rekognition = boto3.client('rekognition', region_name='us-east-1')

# Your verified bucket name
BUCKET_NAME = 'img-rekog-umair'

# The list of images you uploaded to S3 (updated to match the local PNG files)
image_list = ['car.png', 'coffee.png', 'dog.png']

def analyze_images():
    for image_name in image_list:
        print(f"\n--- Analyzing: {image_name} ---")

        try:
            # Call Rekognition to detect labels
            response = rekognition.detect_labels(
                Image={
                    'S3Object': {
                        'Bucket': BUCKET_NAME,
                        'Name': image_name
                    }
                },
                MaxLabels=5,        # Top 5 detected items
                MinConfidence=75    # Only show results with >75% certainty
            )

            # Process and print the detected labels
            if not response['Labels']:
                print("No labels detected with high confidence.")
            else:
                for label in response['Labels']:
                    print(f"Detected: {label['Name']} | Confidence: {label['Confidence']:.2f}%")

        except Exception as e:
            print(f"Error analyzing {image_name}: {e}")

if __name__ == "__main__":
    analyze_images()