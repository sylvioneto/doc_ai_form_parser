from google.cloud import documentai_v1beta3 as documentai
import json, os

from gcs import download_file_from_gcs, updaload_file_to_gcs

def process_document(bucket_name, object_name):

    local_filename = download_file_from_gcs(bucket_name, object_name)

    # Instantiates a client
    client = documentai.DocumentProcessorServiceClient()

    # The full resource name of the processor, e.g.:
    # projects/project-id/locations/location/processor/processor-id
    # You must create new processors in the Cloud Console first
    name = f"projects/{os.getenv('PROJECT_ID')}/locations/us/processors/{os.getenv('PROCESSOR_ID')}"

    with open(local_filename, "rb") as image:
        image_content = image.read()

    # Read the file into memory
    document = {"content": image_content, "mime_type": "application/pdf"}

    # Configure the process request
    request = {"name": name, "document": document}

    # Use the Document AI client to process the sample form
    result = client.process_document(request=request)

    document = result.document
    document_text = document.text
    print("Document processing complete.")
    print("Text: {}".format(document_text))

    data = {}
    document_pages = document.pages
    for page in document_pages:
        print("Page Number:{}".format(page.page_number))
        for form_field in page.form_fields:
            fieldName=get_text(form_field.field_name,document)
            nameConfidence = round(form_field.field_name.confidence,4)
            fieldValue = get_text(form_field.field_value,document)
            valueConfidence = round(form_field.field_value.confidence,4)
            print(fieldName+fieldValue +"  (Confidence Scores: "+str(nameConfidence)+", "+str(valueConfidence)+")")
            data[fieldName] = fieldValue

    result_filename = local_filename.replace("pdf","json")
    with open(result_filename, 'w') as outfile:
        json.dump(data, outfile)    
    
    updaload_file_to_gcs(os.getenv('OUTPUT_BUCKET'), result_filename)


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

