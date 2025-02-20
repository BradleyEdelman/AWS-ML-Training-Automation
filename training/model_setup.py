import os
import yaml
import tensorflow as tf

# Load config
with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

MODEL_NAME = config["training"]["model"]
CHECKPOINT_DIR = config["training"]["checkpoint_dir"]
CHECKPOINT_FILE = config["training"]["checkpoint_file"]
RESUME_TRAINING = config["training"]["resume_from_checkpoint"]


def load_checkpoint(CHECKPOINT_DIR):

    checkpoint_path = os.path.join(CHECKPOINT_DIR, CHECKPOINT_FILE)

    if os.path.exists(checkpoint_path + ".index"):
        print(f"Loading checkpoint from {checkpoint_path}...")
        model.load_weights(checkpoint_path)
        return model
    else:
        print("No checkpoint found. Training from scratch.")
        return None

def create_model(MODEL_NAME):

    print(f"Loading model: {MODEL_NAME}")

    # DETECT NUM OF CLASSES

    model = None
    if MODEL_NAME == "resnet50":
        model = tf.keras.applications.ResNet50(
            include_top=True, weights=None, input_shape=(224, 224, 3), classes=10
        )

    elif MODEL_NAME == "inceptionv3":
        model = tf.keras.applications.InceptionV3(
            include_top=True, weights=None, input_shape=(224, 224, 3), classes=10
        )

    elif MODEL_NAME == "unet":
        # Import custom UNet model
        model = None

    elif MODEL_NAME == "gpt2":
        from transformers import TFGPT2LMHeadModel
        model = TFGPT2LMHeadModel.from_pretrained("gpt2")

    elif MODEL_NAME == "dcgan":
        # Import custom DCGAN model
        model = None
        
    else:
        raise ValueError(f"'{MODEL_NAME}' is not supported.")

    return model



def main():

    model = None

    # Resume from checkpoint if enabled
    if RESUME_TRAINING:
        model = load_checkpoint(CHECKPOINT_DIR=CHECKPOINT_DIR)

    if model is None:
        model = create_model(MODEL_NAME)

    if model:
        # Model summary
        model.summary()
        print("Model setup complete.")

    return model


if __name__ == "__main__":
    model = create_model()
