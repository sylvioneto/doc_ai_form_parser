from google.cloud import storage

tmp_dir = '/tmp'

def download_file_from_gcs(bucket_name, object_name):
    """Lists all the blobs in the bucket."""
    file_name='/{}}/{}'.format(tmp_dir, object_name)
    # storage_client = storage.Client(project=os.getenv('PROJECT_ID'))
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(object_name)
    blob.download_to_filename(file_name)
    return file_name


def updaload_file_to_gcs(bucket_name, file_name):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(file_name.replace(tmp_dir, ""))
    blob.upload_from_filename(file_name)
