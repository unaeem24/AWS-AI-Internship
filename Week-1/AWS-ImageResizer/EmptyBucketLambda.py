import json

def lambda_handler(event, context):
    # TODO implement
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }

import boto3
def lambda_handler(event, context):
    s3 = boto3.resource('s3')
    # Change this to your actual source bucket name
    bucket = s3.Bucket('images-upload-umair') 
    bucket.objects.all().delete()
    return {"status": "Source bucket cleared"}