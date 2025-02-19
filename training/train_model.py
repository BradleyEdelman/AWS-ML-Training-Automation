import os
import tensorflow as tf
import yaml
import subprocess
from tensorflow.keras.callbacks import ModelCheckpoint
from training.prepare_data import load_training_data

# Load config
with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

CHECKPOINT_DIR = config["training"]["checkpoint_dir"]
CHECKPOINT_FILE = config["training"]["checkpoint_file"]
EPOCHS = config["training"]["epochs"]
CHECKPOINT_INTERVAL = config["training"]["checkpoint_interval"]

# Ensure checkpoint directory exists
os.makedirs(CHECKPOINT_DIR, exist_ok=True)

# Prepare data

# Start spot termination detection in the background
subprocess.Popen(["bash", "setup/detect_spot_termination.sh"])

# Define model based on config input
# add callback for checkpointing, or do it manually
# check for checpoints? load last checkpoint if resuming
# Save final model if completed

print("Training finished successfully!")
