import os
import subprocess

import yaml  # type: ignore

from ml import data_check, data_prepare, model_configure, training_loops

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
    subprocess.Popen(["bash", "runtime_spot/monitoring/detect_spot_termination.sh"])

    # Load model and compile model (if applicable)
    model, tokenizer = model_configure.main()

    # Run training loop with custom checkpointing
    if MODEL_NAME in ["resnet50", "resnet101", "inceptionv3", "mobilenetv2"]:
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
