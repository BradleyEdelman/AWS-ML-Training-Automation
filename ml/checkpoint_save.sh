#!/bin/bash

# Load configuration
CONFIG_FILE="config.yaml"

S3_BUCKET=$(yq e '.aws.s3_bucket' $CONFIG_FILE)
CHECKPOINT_DIR=$(yq e '.training.checkpoint_dir' $CONFIG_FILE)
CHECKPOINT_FILE=$(yq e '.training.checkpoint_file' $CONFIG_FILE)

echo "Saving model checkpoint..."
mkdir -p "$CHECKPOINT_DIR"

# Call Python script to save model state
# Currently, this overrides file - I will want to save multiple files to restart from earlier point if desire
python training/save_checkpoint.py "$CHECKPOINT_DIR/$CHECKPOINT_FILE"

echo "Uploading checkpoint to S3: s3://$S3_BUCKET/$CHECKPOINT_FILE"
aws s3 cp "$CHECKPOINT_DIR/$CHECKPOINT_FILE" "s3://$S3_BUCKET/$CHECKPOINT_FILE"

echo "Checkpoint saved!"
