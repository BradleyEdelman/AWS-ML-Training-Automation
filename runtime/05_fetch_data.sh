#!/bin/bash

# Load configuration
CONFIG_FILE="config.yaml"

S3_BUCKET=$(yq e '.aws.s3_bucket' $CONFIG_FILE)
DATASET_PATH=$(yq e '.training.dataset_path' $CONFIG_FILE)
CHECKPOINT_DIR=$(yq e '.training.checkpoint_dir' $CONFIG_FILE)
CHECKPOINT_FILE=$(yq e '.training.checkpoint_file' $CONFIG_FILE)
RESUME_FROM_CHECKPOINT=$(yq e '.training.resume_from_checkpoint' $CONFIG_FILE)

# Ensure dataset directory exists
mkdir -p "$DATASET_PATH"

# Download dataset from S3
echo "Downloading dataset from S3 bucket: $S3_BUCKET..."
aws s3 sync "s3://$S3_BUCKET/" "$DATASET_PATH/"

# If resume flag is set, check and download checkpoint
if [[ "$RESUME_FROM_CHECKPOINT" == "true" ]]; then
    mkdir -p "$CHECKPOINT_DIR"
    echo "Checking for saved checkpoint..."
    aws s3 ls "s3://$S3_BUCKET/$CHECKPOINT_FILE" > /dev/null 2>&1

    # or load most recent checkpoint if specified one doesnt exist???
    if [[ $? -eq 0 ]]; then
        echo "Found checkpoint: $CHECKPOINT_FILE. Downloading..."
        aws s3 cp "s3://$S3_BUCKET/$CHECKPOINT_FILE" "$CHECKPOINT_DIR/$CHECKPOINT_FILE"
        echo "Checkpoint restored: $CHECKPOINT_DIR/$CHECKPOINT_FILE"
    else
        echo "No checkpoint found. Training will start from scratch."
    fi
fi

echo "Data preparation complete!"
