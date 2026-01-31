import json

def lambda_handler(event, context):
    # TODO implement
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
import boto3
import os

import boto3
import os
from PIL import Image
import io

s3 = boto3.client('s3')

def lambda_handler(event, context):
    # 1. Get the bucket and file name from the trigger
    source_bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    
    # 2. Define your destination bucket name (Double check this name!)
    destination_bucket = os.environ['DEST_BUCKET'] 

    # 3. Download the image from S3
    response = s3.get_object(Bucket=source_bucket, Key=key)
    image_content = response['Body'].read()

    # 4. Resize the image using Pillow
    with Image.open(io.BytesIO(image_content)) as img:
        img.thumbnail((128, 128)) # Resize to max 128x128
        buffer = io.BytesIO()
        img.save(buffer, format=img.format)
        resized_image_data = buffer.getvalue() # This defines the missing variable!

    # 5. Upload the "resized_image_data" to the destination bucket
    s3.put_object(
        Bucket=destination_bucket, 
        Key=f"resized-{key}", 
        Body=resized_image_data
    )

    return {"status": "Success!"}