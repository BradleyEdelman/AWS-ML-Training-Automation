import os

import yaml  # type: ignore
from transformers import TFGPT2LMHeadModel

# Load config
with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

S3_BUCKET = config["aws"]["s3_bucket"]
CHECKPOINT_DIR = config["training"]["checkpoint_dir"]
CHECKPOINT_PREFIX = config["training"]["checkpoint_prefix"]
MODEL_NAME = config["training"]["model"]


def checkpoint_load(model):

    checkpoint_files = [
        f for f in os.listdir(CHECKPOINT_DIR) if f.startswith(CHECKPOINT_PREFIX)
    ]
    if not checkpoint_files:
        return model
    checkpoint_files.sort(
        key=lambda f: os.path.getmtime(os.path.join(CHECKPOINT_DIR, f)), reverse=True
    )
    latest_checkpoint_path = os.path.join(CHECKPOINT_DIR, checkpoint_files[0])

    print(f"Found latest checkpoint: {latest_checkpoint_path}")

    # Load weights based on model type
    if MODEL_NAME in ["resnet50", "inceptionv3", "unet"]:
        print(f"Loading CNN checkpoint: {latest_checkpoint_path}")
        model.load_weights(latest_checkpoint_path)

    elif MODEL_NAME == "gpt2":
        print(f"Loading GPT-2 checkpoint from {latest_checkpoint_path}")
        model = TFGPT2LMHeadModel.from_pretrained(latest_checkpoint_path)

    elif MODEL_NAME == "dcgan":
        generator_path = latest_checkpoint_path.replace("_generator.h5", "_generator")
        discriminator_path = latest_checkpoint_path.replace(
            "_discriminator.h5", "_discriminator"
        )
        print(f"Loading GAN generator checkpoint: {generator_path}")
        print(f"Loading GAN discriminator checkpoint: {discriminator_path}")
        model["generator"].load_weights(generator_path)
        model["discriminator"].load_weights(discriminator_path)

    else:
        print("Unknown model type. Skipping checkpoint load.")

    print("Checkpoint successfully loaded!")
    return model
