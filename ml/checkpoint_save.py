import os
import tensorflow as tf
import boto3
import yaml

# Load configuration
with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

S3_BUCKET = config["aws"]["s3_bucket"]
CHECKPOINT_DIR = config["training"]["checkpoint_dir"]
CHECKPOINT_FILE = config["training"]["checkpoint_file"]
EPOCHS = config["training"]["epochs"]
CHECKPOINT_INTERVAL = config["training"]["checkpoint_interval"]

# Ensure checkpoint directory exists
os.makedirs(CHECKPOINT_DIR, exist_ok=True)

# Initialize S3 client
s3 = boto3.client("s3")

def save_checkpoint(model, epoch):
    checkpoint_path = os.path.join(CHECKPOINT_DIR, CHECKPOINT_FILE)
    
    # Save checkpoint locally
    print(f"Saving checkpoint at epoch {epoch}...")
    model.save_weights(checkpoint_path)
    
    # Upload to S3
    print(f"Uploading checkpoint to S3: s3://{S3_BUCKET}/{CHECKPOINT_FILE}...")
    s3.upload_file(checkpoint_path, S3_BUCKET, CHECKPOINT_FILE)
    print("Checkpoint saved successfully!")
