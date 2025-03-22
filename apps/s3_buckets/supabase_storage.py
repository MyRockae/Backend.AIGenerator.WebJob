from supabase import create_client, Client
import io
from django.conf import settings

# Create the Supabase client.
supabase: Client = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)

def ensure_bucket_exists(bucket_name: str):
    # List current buckets (this returns a list of bucket dictionaries).
    buckets = supabase.storage.list_buckets()

    if not any(bucket.id == bucket_name for bucket in buckets):
        create_response = supabase.storage.create_bucket(bucket_name,bucket_name)
        if isinstance(create_response, dict) and create_response.get("error"):
            raise Exception(f"Error creating bucket: {create_response.get('error')}")
        print(f"Bucket '{bucket_name}' created.")
    else:
        print(f"Bucket '{bucket_name}' already exists.")


def upload_file(uploaded_file, file_name: str, bucket_name: str = "generator-input-files"):
    # Ensure the bucket exists.
    ensure_bucket_exists(bucket_name)
    uploaded_file.seek(0)
    file_bytes = uploaded_file.read()
    options = {"contentType": uploaded_file.content_type}
    # Upload the file.
    response = supabase.storage.from_(bucket_name).upload(file_name, file_bytes, options)
    print(response)
    # Check if the response object has an "error" attribute and if it is not empty.
    if hasattr(response, "error") and response.error:
        raise Exception(f"Error uploading file: {response.error}")

    #print(f"File '{file_name}' uploaded successfully.")
    return response


def delete_file(file_name: str, bucket_name: str = "generator-input-files"):
    # Remove expects a list of file paths.
    response = supabase.storage.from_(bucket_name).remove([file_name])
    print(response)
    
    if hasattr(response, "error") and response.error:
        raise Exception(f"Error deleting file: {response.error}")

    #print(f"File '{file_name}' deleted successfully.")
    return response


def download_file(file_name: str, bucket_name: str = "generator-input-files"):
    response = supabase.storage.from_(bucket_name).download(file_name)

    if hasattr(response, "error") and response.error:
        raise Exception(f"Error downloading file: {response.error}")
    
    # Assume the response contains the file bytes in an attribute called 'data'
    file_bytes = response.data if hasattr(response, "data") else response
    #print(f"Downloaded file '{file_name}' from bucket '{bucket_name}'.")
    return io.BytesIO(file_bytes)