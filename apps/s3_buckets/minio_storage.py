from minio import Minio
from minio.error import S3Error
from django.conf import settings

minio_client = Minio(
    settings.MINIO_URL,
    settings.MINIO_ACCESS_KEY,
    settings.MINIO_SECRET_KEY,
    secure=False
)

bucket_name = "generator-input-files"

def ensure_bucket_exists(bucket_name):
    try:
        if not minio_client.bucket_exists(bucket_name):
            minio_client.make_bucket(bucket_name)
            print(f"Bucket '{bucket_name}' created.")
        else:
            print(f"Bucket '{bucket_name}' already exists.")
    except S3Error as err:
        raise Exception(f"Error ensuring bucket exists: {err}")

def upload_file(uploaded_file, bucket_name="generator-input-files"):
    # Ensure the bucket exists.
    ensure_bucket_exists(bucket_name)
    
    file_name = uploaded_file.name
    uploaded_file.seek(0)  # Reset pointer in case it's been read before.
    
    try:
        minio_client.put_object(
            bucket_name,
            file_name,
            uploaded_file,  # use the file stream directly
            uploaded_file.size,
            content_type=uploaded_file.content_type
        )
    except S3Error as err:
        raise Exception(f"Error uploading file: {err}")