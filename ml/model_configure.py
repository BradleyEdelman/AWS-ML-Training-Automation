import os
import yaml
import tensorflow as tf
from transformers import TFGPT2LMHeadModel
import training.checkpoint_load as checkpoint_load

# Load config
with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

MODEL_NAME = config["training"]["model"]
CHECKPOINT_DIR = config["training"]["checkpoint_dir"]
CHECKPOINT_FILE = config["training"]["checkpoint_file"]
RESUME_TRAINING = config["training"]["resume_from_checkpoint"]

def create_model(model_name, num_classes=10):
    print(f"Loading base model: {model_name}")

    if model_name == "resnet50":
        model = tf.keras.applications.ResNet50(
            include_top=True, weights=None, input_shape=(224, 224, 3), classes=num_classes
        )

    elif model_name == "inceptionv3":
        model = tf.keras.applications.InceptionV3(
            include_top=True, weights=None, input_shape=(224, 224, 3), classes=num_classes
        )

    elif model_name == "unet":
        model = None  # Placeholder for UNet model implementation

    elif model_name == "gpt2":
        model = TFGPT2LMHeadModel.from_pretrained("gpt2")

    elif model_name == "dcgan":
        model = {"generator": None, "discriminator": None}  # Placeholder for DCGAN

    else:
        raise ValueError(f"'{model_name}' is not supported.")

    return model



def main():
    # Create a fresh model
    model = create_model(MODEL_NAME)

    # If resuming training, load the checkpoint
    if RESUME_TRAINING:
        model = checkpoint_load.load_checkpoint(model)

    if model:
        print("Model ready.")
        model.summary()

    return model

if __name__ == "__main__":
    model = main()
