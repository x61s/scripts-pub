#!/bin/bash

# Set the Slack upload token
token=<TOKEN>

# Set the channel name where you want to upload the file
channel=<ID>

# Set the path to the text file you want to upload
file_path="file.txt"

# Set the initial message text
message="File to review: $CI_PROJECT_NAME $CI_COMMIT_PROJECT_PATH $CI_PIPELINE_ID $CI_PIPELINE_SOURCE $CI_PIPELINE_URL $CI_COMMIT_REF_SLUG"

curl -v -F file=@$file_path -F "initial_comment=$message" -F channels="$channel" -H "Authorization: Bearer $token" https://slack.com/api/files.upload

