import os
import tensorflow as tf
import yaml
import subprocess
import training.data_prepare as data_prepare
import training.data_check as data_check
import training.model_configure as model_configure
import training.training_loops as training_loops 

# Load config
with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

CHECKPOINT_DIR = config["training"]["checkpoint_dir"]
MODEL_NAME = config["training"]["model"]


def main():

    # Check dataset format
    print("Checking dataset formatting...")
    if not data_check.main():
        print("Data format validation failed. Exiting...")
        return

    # Prepare dataset
    print("Preparing dataset for training...")
    dataset = data_prepare.main()

    # Ensure checkpoint directory exists
    os.makedirs(CHECKPOINT_DIR, exist_ok=True)

    # Start AWS Spot termination detection in the background
    print("Detecting AWS Spot termination in background...")
    subprocess.Popen(["bash", "setup/detect_spot_termination.sh"])

    # Load model
    model = model_configure.main()

    # Run training loop with custom checkpointing
    if MODEL_NAME in ["resnet50", "inceptionv3"]:
        training_loops.train_cnn(model, dataset)
    elif MODEL_NAME == "gpt2":
        training_loops.train_gpt2(model, dataset)
    elif MODEL_NAME == "dcgan":
        training_loops.train_dcgan(model, dataset)
    else:
        print(f"No training script available for '{MODEL_NAME}'. Exiting...")
        return


if __name__ == "__main__":
    main()
