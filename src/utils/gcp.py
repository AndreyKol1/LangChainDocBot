from google.cloud import storage
import os

storage_client = storage.Client()

def download_directory_from_gcs(gcs_directory, local_directory, bucket_name):
    if not os.path.exists(local_directory):
        bucket = storage_client.bucket(bucket_name)
        blobs = bucket.list_blobs(prefix=gcs_directory)

        for blob in blobs:
            if not blob.name.endswith("/"): 
                relative_path = os.path.relpath(blob.name, gcs_directory)
                local_file_path = os.path.join(local_directory, relative_path)
                os.makedirs(os.path.dirname(local_file_path), exist_ok=True)
                blob.download_to_filename(local_file_path)
                print(f"Downloaded {blob.name} to {local_file_path}")