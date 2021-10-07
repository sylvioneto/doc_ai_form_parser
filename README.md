How to deploy:
gcloud functions deploy doc_ai_test \
--runtime python38 \
--entry-point main \
--trigger-resource <YOUR-BUCKET-NAME> \
--trigger-event google.storage.object.finalize \
--set-env-vars PROCESSOR_ID=<YOUR-PROCESSOR-ID>,PROJECT_ID=<YOUR-PROJECT-ID>

Example:
gcloud functions deploy doc_ai_test \
--runtime python38 \
--entry-point main \
--trigger-resource syl-data-tests-doc-ai \
--trigger-event google.storage.object.finalize \
--set-env-vars PROCESSOR_ID=7776fd072ecba23f,PROJECT_ID=syl-data-tests
