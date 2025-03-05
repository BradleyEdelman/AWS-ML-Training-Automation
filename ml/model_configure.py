import os

import tensorflow as tf
import yaml  # type: ignore
from transformers import AutoModelForCausalLM, AutoTokenizer

from ml import checkpoint_load

# Load config
with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

MODEL_NAME = config["training"]["model"]
FINE_TUNE = config["training"]["fine_tune"]
DATA_PATH = config["training"]["dataset_path"]
CHECKPOINT_DIR = config["training"]["checkpoint_dir"]
CHECKPOINT_PREFIX = config["training"]["checkpoint_prefix"]
RESUME_TRAINING = config["training"]["resume_from_checkpoint"]


def model_create(model_name, num_classes=None):
    print(f"Loading base model: {model_name}")

    if model_name == "resnet50":

        if num_classes is None:
            return None
        else:
            model = tf.keras.applications.ResNet50(
                include_top=True,
                weights=None,
                input_shape=(224, 224, 3),
                classes=num_classes,
            )
        tokenizer = None

    elif model_name == "resnet101":

        if num_classes is None:
            return None
        else:
            model = tf.keras.applications.ResNet101(
                include_top=True,
                weights=None,
                input_shape=(224, 224, 3),
                classes=num_classes,
            )
        tokenizer = None

    elif model_name == "inceptionv3":

        if num_classes is None:
            return None
        else:
            model = tf.keras.applications.InceptionV3(
                include_top=True,
                weights=None,
                input_shape=(224, 224, 3),
                classes=num_classes,
            )
        tokenizer = None

    elif model_name == "mobilenetv2":

        if num_classes is None:
            return None
        else:
            model = tf.keras.applications.MobileNetV2(
                include_top=True,
                weights=None,
                input_shape=(224, 224, 3),
                classes=num_classes,
            )
        tokenizer = None

    elif model_name == "unet":
        model = None  # Placeholder for UNet model implementation
        tokenizer = None

    elif model_name in [
        "gpt2",
        "EleutherAI/gpt-j-6B",
        "mistralai/Mistral-7B",
        "meta-llama/Llama-2-7b-hf",
        "meta-llama/Llama-2-13b-hf",
    ]:
        model = AutoModelForCausalLM.from_pretrained(model_name)
        tokenizer = AutoTokenizer.from_pretrained(model_name)

    elif model_name == "dcgan":
        model = {"generator": None, "discriminator": None}  # Placeholder for DCGAN

    else:
        raise ValueError(f"'{model_name}' is not supported.")

    return model, tokenizer


def model_fine_tune(model, model_name):

    if model_name in ["resnet50", "resnet101", "inceptionv3", "mobilenetv2"]:

        with open("config_cnn.yaml", "r") as f:
            config_cnn = yaml.safe_load(f)

        NUM_LAYERS_TO_UNFREEZE = config_cnn["num_layers_to_unfreeze"]

        for layer in model.layers[-NUM_LAYERS_TO_UNFREEZE:]:
            if not isinstance(
                layer, tf.keras.layers.BatchNormalization
            ):  # Keep batch norm frozen
                layer.trainable = True
        print(
            f"Fine-tuning enabled. Unfroze the top {NUM_LAYERS_TO_UNFREEZE} layers of {model_name}."
        )

    elif model_name in [
        "gpt2",
        "EleutherAI/gpt-j-6B",
        "mistralai/Mistral-7B",
        "meta-llama/Llama-2-7b-hf",
        "meta-llama/Llama-2-13b-hf",
    ]:

        with open("config_llm.yaml", "r") as f:
            config_llm = yaml.safe_load(f)

        NUM_LAYERS_TO_UNFREEZE = config_llm["num_layers_to_unfreeze"]

        for layer in model.transformer.h[
            :-NUM_LAYERS_TO_UNFREEZE
        ]:  # Freeze earlier transformer blocks
            for param in layer.parameters():
                param.requires_grad = False
        print(
            f"Fine-tuning enabled. Unfroze the last {NUM_LAYERS_TO_UNFREEZE} transformer blocks of {model_name}."
        )

    return model


def model_compile(model, model_name):

    if model_name in ["resnet50", "resnet101", "inceptionv3", "mobilenetv2"]:

        with open("config_cnn.yaml", "r") as f:
            config_cnn = yaml.safe_load(f)

        OPTIMIZER = config_cnn["optimizer"]
        LEARNING_RATE = config_cnn["learning_rate"]
        LOSS_FUNCTION = config_cnn["loss_function"]
        METRICS = config_cnn["metrics"]

        optimizer = tf.keras.optimizers.get(
            {"class_name": OPTIMIZER, "config": {"learning_rate": LEARNING_RATE}}
        )
        model.compile(
            optimizer=optimizer,
            loss=LOSS_FUNCTION,
            metrics=METRICS,
        )
        print(f"{model_name} compiled.")

    elif model_name == "dcgan":
        optimizer = tf.keras.optimizers.get(
            {"class_name": OPTIMIZER, "config": {"learning_rate": LEARNING_RATE}}
        )
        model["generator"].compile(optimizer=optimizer, loss=LOSS_FUNCTION)
        model["discriminator"].compile(optimizer=optimizer, loss=LOSS_FUNCTION)
        print(f"{model_name} compiled with binary crossentropy loss.")

    else:
        print(f"{model_name} does not require compilation.")

    return model


def main():

    # Create a fresh model
    if MODEL_NAME in ["resnet50", "resnet101", "inceptionv3", "mobilenetv2"]:
        num_classes = len(
            [
                d
                for d in os.listdir(DATA_PATH)
                if os.path.isdir(os.path.join(DATA_PATH, d))
            ]
        )
        if num_classes is None or num_classes == 0:
            print("Could not determine number of classes!")
            return None
    else:
        num_classes = None

    model, tokenizer = model_create(MODEL_NAME, num_classes=num_classes)

    # Specify fine-tuning parameters (unfreezing layers)
    if FINE_TUNE:
        model = model_fine_tune(model, MODEL_NAME)

    # If resuming training, load the checkpoint
    if RESUME_TRAINING:
        model = checkpoint_load.checkpoint_load(model)

    # compile model (if applicable)
    model = model_compile(model, MODEL_NAME)

    print("Model configuration complete.")
    # model.summary()

    return model, tokenizer


if __name__ == "__main__":
    model = main()
