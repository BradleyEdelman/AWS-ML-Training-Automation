#!/bin/bash

# Load config
CONFIG_FILE="config.yaml"
REGION=$(yq e '.aws.region' "$CONFIG_FILE")
PROJECT=$(yq e '.project' "$CONFIG_FILE")
S3_BUCKET_LOGS=$(yq e '.aws.s3_bucket_logs' "$CONFIG_FILE")

LOG_GROUP="/aws/ml-training"
LOCAL_DIR="runtime_spot/logs"
mkdir -p "$LOCAL_DIR"

# Extract bucket and prefix if provided (e.g., "bucket-name/logs" → "bucket-name", "logs")
BUCKET_NAME=$(echo "$S3_BUCKET_LOGS" | cut -d'/' -f1)
BUCKET_PREFIX=$(echo "$S3_BUCKET_LOGS" | cut -s -d'/' -f2-)

echo "Syncing CloudWatch logs for project: $PROJECT"
echo "Searching in log group: $LOG_GROUP"

# Ensure S3 bucket exists
echo "Checking if S3 bucket '$BUCKET_NAME' exists..."
if ! aws s3api head-bucket --bucket "$BUCKET_NAME" 2>/dev/null; then
	echo "Creating bucket $BUCKET_NAME in region $REGION..."
	aws s3api create-bucket \
		--bucket "$BUCKET_NAME" \
		--region "$REGION" \
		--create-bucket-configuration LocationConstraint="$REGION"
	echo "Bucket created."
else
	echo "Bucket exists: $BUCKET_NAME"
fi

# List log streams for this project
STREAM_NAMES=$(aws logs describe-log-streams \
	--log-group-name "$LOG_GROUP" \
	--region "$REGION" \
	--query "logStreams[?starts_with(logStreamName, \`${PROJECT}_\`)].logStreamName" \
	--output text)

if [[ -z "$STREAM_NAMES" ]]; then
	echo "No log streams found for project: $PROJECT"
	exit 0
fi

for STREAM in $STREAM_NAMES; do
	echo "Downloading log stream: $STREAM"

	LOCAL_FILE="$LOCAL_DIR/${STREAM}.txt"
	aws logs get-log-events \
		--log-group-name "$LOG_GROUP" \
		--log-stream-name "$STREAM" \
		--region "$REGION" \
		--query "events[*].message" \
		--output text >"$LOCAL_FILE"

	if [[ -s "$LOCAL_FILE" ]]; then
		# Final S3 path (bucket/logs/project/stream.txt)
		if [[ -n "$BUCKET_PREFIX" ]]; then
			S3_DEST="s3://${BUCKET_NAME}/${BUCKET_PREFIX}/${PROJECT}/${STREAM}.txt"
		else
			S3_DEST="s3://${BUCKET_NAME}/logs/${PROJECT}/${STREAM}.txt"
		fi

		echo "Uploading $STREAM to $S3_DEST"
		aws s3 cp "$LOCAL_FILE" "$S3_DEST"
	else
		echo "Log stream $STREAM is empty or failed to fetch."
		rm -f "$LOCAL_FILE"
	fi
done

echo "All available logs for '$PROJECT' synced to: s3://${BUCKET_NAME}/${BUCKET_PREFIX:-logs}/${PROJECT}/"
