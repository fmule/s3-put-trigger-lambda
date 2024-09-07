import os
# from openai import OpenAI

def transcribe_audio(bucket_name, file_key, s3_client):
    local_file_name = f"/tmp/{file_key.split('/')[-1]}"
    
    # Download the file from S3
    s3_client.download_file(Bucket=bucket_name, Key=file_key, Filename=local_file_name)
    print(f"File downloaded: {local_file_name}")

    if not (local_file_name.lower().endswith('.mp3') or local_file_name.lower().endswith('.wav')):
        print('Only MP3 and WAV files are supported')
        return

    # Initialize OpenAI client
    # client_openai = OpenAI()

    # Perform transcription
    with open(local_file_name, "rb") as audio_file:
        transcription = "Transcription not implemented yet"        
        # transcription = client_openai.audio.transcriptions.create(
        #     model="whisper-1",
        #     file=audio_file
        # )

    # Archive the original audio file
    archived_file_key = f'archived/{local_file_name.split('/')[-1].split('.')[0]}' + '.ark'      
    s3_client.upload_file(local_file_name, bucket_name, archived_file_key)
    print(f'{local_file_name} uploaded to = {bucket_name}/{archived_file_key}')  
   

    # Save transcription to a file
    transcription_file_name = local_file_name.replace('.' + local_file_name.split('.')[-1], '.txt')
    with open(transcription_file_name, 'w') as f:
        f.write(transcription)
    
    # Upload the transcription file to S3
    transcription_file_key = f'transcripts/{transcription_file_name.split("/")[-1]}'
    s3_client.upload_file(transcription_file_name, bucket_name, transcription_file_key)
    print(f"Transcript uploaded: {bucket_name}/{transcription_file_key}")

    # Clean up local files
    
    s3_client.delete_object(Bucket=bucket_name, Key=file_key)    
    os.remove(local_file_name)
    os.remove(transcription_file_name)
    print(f'File Deleted {bucket_name}/{file_key}')

    
