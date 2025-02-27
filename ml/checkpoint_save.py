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
CHECKPOINT_PREFIX = config["training"]["checkpoint_prefix"]
MODEL_NAME = config["training"]["model"]

# Ensure checkpoint directory exists
os.makedirs(CHECKPOINT_DIR, exist_ok=True)

# Initialize S3 client
s3 = boto3.client("s3")


def save_checkpoint(model, epoch=None):
    timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")

    if MODEL_NAME in ["resnet50", "inceptionv3", "unet"]:
        checkpoint_filename = f"{CHECKPOINT_PREFIX}_epoch{epoch}_{timestamp}.h5"
        model.save_weights(os.path.join(CHECKPOINT_DIR, checkpoint_filename))

    elif MODEL_NAME == "gpt2":
        checkpoint_filename = f"{CHECKPOINT_PREFIX}_epoch{epoch}_{timestamp}"
        model.save_pretrained(os.path.join(CHECKPOINT_DIR, checkpoint_filename))

    elif MODEL_NAME == "dcgan":
        generator_filename = f"{CHECKPOINT_PREFIX}_epoch{epoch}_{timestamp}_generator.h5"
        model["generator"].save_weights(os.path.join(CHECKPOINT_DIR, generator_filename))

        discriminator_filename = f"{CHECKPOINT_PREFIX}_epoch{epoch}_{timestamp}_discriminator.h5"
        model["discriminator"].save_weights(os.path.join(CHECKPOINT_DIR, discriminator_filename))

    else:
        print(f"Checkpoint saving is not implemented for '{MODEL_NAME}'")
        return

    # Upload to S3
    print(f"Uploading checkpoint to S3: s3://{S3_BUCKET}/{checkpoint_filename}...")
    # rearrange names a bit
    s3_bucket = S3_BUCKET.split('/',1)[0]
    s3_checkpoint_filename = f"{S3_BUCKET.split('/',1)[1]}{'/'}{checkpoint_filename}"
    s3.upload_file(os.path.join(CHECKPOINT_DIR, checkpoint_filename), s3_bucket, s3_checkpoint_filename)
    print("Checkpoint uploaded successfully!")
