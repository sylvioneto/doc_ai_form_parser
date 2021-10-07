from google.cloud import storage
from google.cloud import documentai_v1 as documentai
import json, os


def main(event, context):
    """Background Cloud Function to be triggered by Cloud Storage.
       This generic function logs relevant data when a file is changed.

    Args:
        event (dict):  The dictionary with data specific to this type of event.
                       The `data` field contains a description of the event in
                       the Cloud Storage `object` format described here:
                       https://cloud.google.com/storage/docs/json_api/v1/objects#resource
        context (google.cloud.functions.Context): Metadata of triggering event.
    Returns:
        None; the output is written to Stackdriver Logging
    """

    print('Event ID: {}'.format(context.event_id))
    print('Event type: {}'.format(context.event_type))
    print('Bucket: {}'.format(event['bucket']))
    print('File: {}'.format(event['name']))
    print('Metageneration: {}'.format(event['metageneration']))
    print('Created: {}'.format(event['timeCreated']))
    print('Updated: {}'.format(event['updated']))

    file_name = download_file_from_gcs(event['bucket'], event['name'])
    result_file_name = process_document(file_name)
    updaload_file_to_gcs(event['bucket'], result_file_name)


def download_file_from_gcs(bucket_name, object_name):
    """Lists all the blobs in the bucket."""
    file_name = '/tmp/{}'.format(object_name)
    storage_client = storage.Client(project=os.getenv('PROJECT_ID'))
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(object_name)
    blob.download_to_filename(file_name)
    return file_name


def updaload_file_to_gcs(bucket_name, file_name):
    storage_client = storage.Client(project=os.getenv('PROJECT_ID'))
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(file_name)
    blob.upload_from_filename(file_name)


def process_document(file_name=None):
    location=os.getenv('PROCESSOR_LOCATION', 'us')

    # You must set the api_endpoint if you use a location other than 'us', e.g.:
    opts = {}
    if location == "eu":
        opts = {"api_endpoint": "eu-documentai.googleapis.com"}

    client = documentai.DocumentProcessorServiceClient(client_options=opts)

    # The full resource name of the processor, e.g.:
    # projects/project-id/locations/location/processor/processor-id
    # You must create new processors in the Cloud Console first
    name = f"projects/{os.getenv('PROJECT_ID')}/locations/{location}/processors/{os.getenv('PROCESSOR_ID')}"

    # Read the file into memory
    with open(file_name, "rb") as image:
        image_content = image.read()

    document = {"content": image_content, "mime_type": "application/pdf"}

    # Configure the process request
    request = {"name": name, "raw_document": document}

    result = client.process_document(request=request)
    document = result.document
    document_pages = document.pages

    # For a full list of Document object attributes, please reference this page: https://googleapis.dev/python/documentai/latest/_modules/google/cloud/documentai_v1beta3/types/document.html#Document

    # Read the text recognition output from the processor
    data = {}
    data['paragraphs'] = []
    print("The document contains the following paragraphs:")
    for page in document_pages:
        paragraphs = page.paragraphs
        for paragraph in paragraphs:
            print(paragraph)
            paragraph_text = get_text(paragraph.layout, document)
            print(f"Paragraph text: {paragraph_text}")
            data['paragraphs'].append(paragraph_text)

    result_file_name = file_name.replace("pdf","json")
    with open(result_file_name, 'w') as outfile:
        json.dump(data, outfile)
    return result_file_name


def get_text(doc_element: dict, document: dict):
    """
    Document AI identifies form fields by their offsets
    in document text. This function converts offsets
    to text snippets.
    """
    response = ""
    # If a text segment spans several lines, it will
    # be stored in different text segments.
    for segment in doc_element.text_anchor.text_segments:
        start_index = (
            int(segment.start_index)
            if segment in doc_element.text_anchor.text_segments
            else 0
        )
        end_index = int(segment.end_index)
        response += document.text[start_index:end_index]
    return response

