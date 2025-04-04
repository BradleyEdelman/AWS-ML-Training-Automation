import datetime
import os

import boto3
import yaml  # type: ignore
from botocore.exceptions import ClientError

# Load config
with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

S3_BUCKET_CHECKPOINT = config["aws"]["s3_bucket_checkpoint"]
CHECKPOINT_DIR = config["training"]["checkpoint_dir"]
CHECKPOINT_PREFIX = config["training"]["checkpoint_prefix"]
MODEL_NAME = config["training"]["model"]


# Ensure checkpoint directory exists
os.makedirs(CHECKPOINT_DIR, exist_ok=True)

# Initialize S3 client
s3 = boto3.client("s3")


# Ensure that the S3 bucket checkpoint saving location exists
def ensure_bucket_exists(bucket_name):
    try:
        s3.head_bucket(Bucket=bucket_name)
    except ClientError as e:
        error_code = int(e.response["Error"]["Code"])
        if error_code == 404:
            print(f"Bucket '{bucket_name}' not found. Creating it...")
            REGION = config["aws"]["region"]
            s3.create_bucket(
                Bucket=bucket_name,
                CreateBucketConfiguration={"LocationConstraint": REGION},
            )
            print(f"Bucket '{bucket_name}' created.")
        else:
            raise


ensure_bucket_exists(S3_BUCKET_CHECKPOINT)


def checkpoint_save(model, epoch=None):
    timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")

    if MODEL_NAME in ["resnet50", "resnet101", "mobilenet_v2", "inceptionv3", "unet"]:
        checkpoint_filename = f"{CHECKPOINT_PREFIX}_epoch{epoch}_{timestamp}.h5"
        model.save_weights(os.path.join(CHECKPOINT_DIR, checkpoint_filename))

    elif MODEL_NAME in [
        "gpt2",
        "EleutherAI/gpt-j-6B",
        "mistralai/Mistral-7B",
        "meta-llama/Llama-2-7b-hf",
        "meta-llama/Llama-2-13b-hf",
    ]:
        checkpoint_filename = f"{CHECKPOINT_PREFIX}_epoch{epoch}_{timestamp}"
        model.save_pretrained(os.path.join(CHECKPOINT_DIR, checkpoint_filename))

    elif MODEL_NAME == "dcgan":
        generator_filename = (
            f"{CHECKPOINT_PREFIX}_epoch{epoch}_{timestamp}_generator.h5"
        )
        model["generator"].save_weights(
            os.path.join(CHECKPOINT_DIR, generator_filename)
        )

        discriminator_filename = (
            f"{CHECKPOINT_PREFIX}_epoch{epoch}_{timestamp}_discriminator.h5"
        )
        model["discriminator"].save_weights(
            os.path.join(CHECKPOINT_DIR, discriminator_filename)
        )

    else:
        print(f"Checkpoint saving is not implemented for '{MODEL_NAME}'")
        return

    # Upload to S3
    print(
        f"Uploading checkpoint to S3: s3://{S3_BUCKET_CHECKPOINT}/{checkpoint_filename}..."
    )
    s3_checkpoint_filename = f"{S3_BUCKET_CHECKPOINT}{'/'}{checkpoint_filename}"
    s3.upload_file(
        os.path.join(CHECKPOINT_DIR, checkpoint_filename),
        S3_BUCKET_CHECKPOINT,
        s3_checkpoint_filename,
    )
    print("Checkpoint uploaded successfully!")
