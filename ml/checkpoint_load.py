import os
import tensorflow as tf
import yaml
from transformers import TFGPT2LMHeadModel

# Load config
with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

S3_BUCKET = config["aws"]["s3_bucket"]
CHECKPOINT_DIR = config["training"]["checkpoint_dir"]
CHECKPOINT_FILE = config["training"]["checkpoint_file"]
MODEL_NAME = config["training"]["model"]

def load_checkpoint(model, CHECKPOINT_DIR, CHECKPOINT_FILE):
    """
    Loads the latest checkpoint for the given model.
    """
    if model is None:
        print("Error: Model must be initialized before loading weights.")
        return None

    checkpoint_path = os.path.join(CHECKPOINT_DIR, CHECKPOINT_FILE)

    if not os.path.exists(CHECKPOINT_DIR):
        print(f"Checkpoint directory {CHECKPOINT_DIR} not found. Starting fresh.")
        return model

    latest_checkpoint = sorted([f for f in os.listdir(CHECKPOINT_DIR) if f.startswith(CHECKPOINT_FILE)], reverse=True)

    if not latest_checkpoint:
        print("No checkpoint found. Starting fresh.")
        return model

    latest_checkpoint_path = os.path.join(CHECKPOINT_DIR, latest_checkpoint[0])

    if MODEL_NAME in ["resnet50", "inceptionv3", "unet"]:
        print(f"Loading CNN checkpoint: {latest_checkpoint_path}")
        model.load_weights(latest_checkpoint_path)

    elif MODEL_NAME == "gpt2":
        print(f"Loading GPT-2 checkpoint from {latest_checkpoint_path}")
        model = TFGPT2LMHeadModel.from_pretrained(latest_checkpoint_path)

    elif MODEL_NAME == "dcgan":
        generator_path = latest_checkpoint_path.replace("_generator.h5", "")
        discriminator_path = latest_checkpoint_path.replace("_discriminator.h5", "")
        print(f"Loading GAN generator checkpoint: {generator_path}")
        print(f"Loading GAN discriminator checkpoint: {discriminator_path}")
        model["generator"].load_weights(generator_path)
        model["discriminator"].load_weights(discriminator_path)

    else:
        print("Unknown model type. Skipping checkpoint load.")

    print(f"Checkpoint {latest_checkpoint_path} loaded successfully!")
    return model
