import tensorflow as tf
import yaml
import os
import numpy as np

# Load config
with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

MODEL_TYPE = config["training"]["model"]
DATA_PATH = config["training"]["dataset_path"]
PREPARED_DATA_PATH = os.path.join(DATA_PATH, "processed")

os.makedirs(PREPARED_DATA_PATH, exist_ok=True)

def prepare_resnet_data():
    print("Preparing Image Data for ResNet50...")

    print("ResNet Data Preparation Complete.")

def prepare_gpt2_data():
    print("Preparing Text Data for GPT-2...")

    print("GPT-2 Data Preparation Complete.")

def prepare_stable_diffusion_data():
    print("Preparing Data for Stable Diffusion...")

    print("Stable Diffusion Data Preparation is model-dependent and requires latents.")
