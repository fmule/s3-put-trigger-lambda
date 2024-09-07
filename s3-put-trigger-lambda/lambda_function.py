import json
import boto3
from transcribe_audio import transcribe_audio
import urllib.parse

# Initialize S3 client
s3 = boto3.client('s3')

def lambda_handler(event, context):
    # Extract bucket name and file key from the event
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    file_key = event['Records'][0]['s3']['object']['key']
    
    print(f'From Lambda : {bucket_name}/{file_key}')
    
    # Normalize file key when its url-encoded
    decoded_file_key = urllib.parse.unquote_plus(file_key)
    print(f'{file_key} decoded too => {decoded_file_key}')
    file_key = decoded_file_key

    # Call the transcribe_audio function
    transcribe_audio(bucket_name, file_key, s3)

    return {
        'statusCode': 200,
        'body': json.dumps('Processing complete')
    }