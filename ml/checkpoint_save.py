import os
import datetime
import tensorflow as tf
import boto3
import yaml
from transformers import TFGPT2LMHeadModel

# Load config
with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

S3_BUCKET = config["aws"]["s3_bucket"]
CHECKPOINT_DIR = config["training"]["checkpoint_dir"]
CHECKPOINT_FILE = config["training"]["checkpoint_file"]
MODEL_NAME = config["training"]["model"]

# Ensure checkpoint directory exists
os.makedirs(CHECKPOINT_DIR, exist_ok=True)

# Initialize S3 client
s3 = boto3.client("s3")

def save_checkpoint(model, epoch=None):
    
    timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    
    if MODEL_NAME in ["resnet50", "inceptionv3", "unet"]:
        checkpoint_filename = f"{CHECKPOINT_FILE}_epoch{epoch}_{timestamp}.h5"
        model.save_weights(os.path.join(CHECKPOINT_DIR, checkpoint_filename))
    
    elif MODEL_NAME == "gpt2":
        checkpoint_filename = f"{CHECKPOINT_FILE}_epoch{epoch}_{timestamp}"
        model.save_pretrained(os.path.join(CHECKPOINT_DIR, checkpoint_filename))
    
    elif MODEL_NAME == "dcgan":
        checkpoint_filename = f"{CHECKPOINT_FILE}_epoch{epoch}_{timestamp}_generator.h5"
        generator.save_weights(os.path.join(CHECKPOINT_DIR, checkpoint_filename))
        checkpoint_filename = f"{CHECKPOINT_FILE}_epoch{epoch}_{timestamp}_iscriminator.h5"
        discriminator.save_weights(os.path.join(CHECKPOINT_DIR, checkpoint_filename))
    
    print(f"Checkpoint saved: {checkpoint_filename}")

    # Upload to S3
    print(f"Uploading checkpoint to S3: s3://{S3_BUCKET}/{checkpoint_filename}...")
    s3.upload_file(os.path.join(CHECKPOINT_DIR, checkpoint_filename), S3_BUCKET, checkpoint_filename)
    print("Checkpoint uploaded successfully!")
