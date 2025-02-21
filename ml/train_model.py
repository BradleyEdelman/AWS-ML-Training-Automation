import os
import tensorflow as tf
import yaml
import subprocess
from tensorflow.keras.callbacks import ModelCheckpoint
import training.data_prepare as data_prepare
import training.data_check as data_check
import training.model_configure as model_configure
import training.checkpoint_save as checkpoint_save

# Load config
with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

CHECKPOINT_DIR = config["training"]["checkpoint_dir"]
CHECKPOINT_FILE = config["training"]["checkpoint_file"]
EPOCHS = config["training"]["epochs"]
CHECKPOINT_INTERVAL = config["training"]["checkpoint_interval"]
MODEL_NAME = config["training"]["model"]
DATA_PATH = config["training"]["dataset_path"]


def main():
    
    # Check data format
    print("Checking dataset formatting...")
    if not data_check.main():
        print("Data format validation failed. Exiting...")
        return

    # Prepare data
    print("Preparing dataset for training...")
    dataset = data_prepare.main()
    
    # Ensure checkpoint directory exists
    os.makedirs(CHECKPOINT_DIR, exist_ok=True)

    # Start spot termination detection in the background
    print("Detecting AWS Spot termination in background)...")
    subprocess.Popen(["bash", "setup/detect_spot_termination.sh"])

    # Define model based on config input and load checkpoint
    model = model_configure.main()
    
    # Train model, manual checkpointing
    for epoch in range(1, EPOCHS + 1):
        print(f"Training Epoch {epoch}/{EPOCHS}")
        model.fit(dataset, epochs=1)

        # Save checkpoint every X epochs
        if epoch % CHECKPOINT_INTERVAL == 0:
            checkpoint_save.save_checkpoint(model, epoch=epoch)

    print("Training completed!")
    checkpoint_save.save_checkpoint(model, epoch="final")  # Final checkpoint save


if __name__ == "__main__":
    main()