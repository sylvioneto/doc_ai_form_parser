

How to run:

1. Create two buckets to receive forms, for example:
- <YOUR-PROJECT-ID>-doc-ai-input
- <YOUR-PROJECT-ID>-doc-ai-output

2. Create a Form Parser Document AI processor.

3. Deploy this Cloud Function informing your PROJECT_ID, PROCESSOR_ID, and BUCKET_NAME.
gcloud functions deploy doc_ai_form_parser \
--runtime python38 \
--trigger-resource <INPUT-BUCKET-NAME> \
--trigger-event google.storage.object.finalize \
--set-env-vars PROCESSOR_ID=<DOC-AI-PROCESSOR-ID>,PROJECT_ID=<YOUR-PROJECT-ID>,OUTPUT_BUCKET=<OUTPUT-BUCKET-NAME>

4. Upload the form_Sally.pdf to the input bucket.

5. Check the result in the output bucket. You'll see a json named after the form. This json has key=value pairs parsed from the form.
