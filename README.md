

How to run:

1. Create two [GCS buckets](https://console.cloud.google.com/storage/browser), for example:
- `<YOUR-PROJECT-ID>`-doc-ai-input: it receives forms and triggers a Cloud Function.
- `<YOUR-PROJECT-ID>`-doc-ai-output: it receives json with parsed form's data.

2. Create a [Document AI processor - Form Parser](https://console.cloud.google.com/ai/document-ai).

3. Deploy this Cloud Function informing your PROJECT_ID, PROCESSOR_ID, and BUCKET_NAME.
```
$ gcloud functions deploy doc_ai_form_parser \
--runtime python38 \
--trigger-resource <INPUT-BUCKET-NAME> \
--trigger-event google.storage.object.finalize \
--set-env-vars PROCESSOR_ID=<DOC-AI-PROCESSOR-ID>,PROJECT_ID=<YOUR-PROJECT-ID>,OUTPUT_BUCKET=<OUTPUT-BUCKET-NAME>
```

4. Upload the form_Sally.pdf file to the input bucket.

5. Check the result in the output bucket. You'll see a json named after the form. This json has key=value pairs parsed from the form.
Example:
```json
{
  "Phone #: ": "(906) 917-3486\n",
  "Emergency Contact: ": "Eva Walker ",
  "Marital Status:\n": "Single ",
  "Gender: ": "F\n",
  "Occupation: ": "Software Engineer\n",
  "Referred By: ": "None\n",
  "Date:\n": "9/14/19\n",
  "DOB: ": "09/04/1986\n",
  "Address: ": "24 Barney Lane ",
  "City: ": "Towaco ",
  "Name:\n": "Sally\nWalker\n",
  "State: ": "NJ ",
  "Email: ": "Sally, waller@cmail.com ",
  "Zip: ": "07082\n",
  "Emergency Contact Phone: ": "(906) 334-8976\n",
  "Are you currently taking any medication? (If yes, please describe):\n": "Vyvanse (25mg) daily for attention\n",
  "Describe your medical concerns (symptoms, diagnoses, etc):\n": "Runny nose, mucas in thwat, weakness,\naches, chills, tired\n"
}
```
