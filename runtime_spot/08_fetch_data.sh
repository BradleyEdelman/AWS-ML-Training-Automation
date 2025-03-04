#!/bin/bash

# Load configuration
CONFIG_FILE="config.yaml"

S3_BUCKET=$(yq e '.aws.s3_bucket' $CONFIG_FILE)
DATASET_PATH=$(yq e '.training.dataset_path' $CONFIG_FILE)
CHECKPOINT_DIR=$(yq e '.training.checkpoint_dir' $CONFIG_FILE)
CHECKPOINT_PREFIX=$(yq e '.training.checkpoint_prefix' $CONFIG_FILE)
RESUME_FROM_CHECKPOINT=$(yq e '.training.resume_from_checkpoint' $CONFIG_FILE)

# Ensure dataset directory exists
mkdir -p "$DATASET_PATH"

# Download dataset from S3 (ignore checkpoint files)
echo "Downloading dataset from S3 bucket: $S3_BUCKET..."
aws s3 sync "s3://$S3_BUCKET/" "$DATASET_PATH/" --exclude "checkpoint*"

# If "resume" traiing flag is set to yes, find and download the most recent checkpoint file
if [[ "$RESUME_FROM_CHECKPOINT" == "true" ]]; then
	mkdir -p "$CHECKPOINT_DIR"
	echo "Finding the latest checkpoint..."

	# List checkpoints, sort by last modified date, download the most recent file
	LATEST_CHECKPOINT=$(aws s3 ls "s3://$S3_BUCKET/" | grep "$CHECKPOINT_PREFIX" | sort -k1,2 | tail -n 1 | awk '{print $4}')

	if [[ -n "$LATEST_CHECKPOINT" ]]; then
		echo "Found latest checkpoint: $LATEST_CHECKPOINT. Downloading..."
		aws s3 cp "s3://$S3_BUCKET/$LATEST_CHECKPOINT" "$CHECKPOINT_DIR/$LATEST_CHECKPOINT"
		echo "Checkpoint file downloaded: $CHECKPOINT_DIR/$LATEST_CHECKPOINT"
	else
		echo "No checkpoint found. Training will start from scratch."
	fi
fi

echo "Data download complete!"
