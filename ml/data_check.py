import json
import os

import yaml  # type: ignore
from PIL import Image

# Load config
with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

MODEL_NAME = config["training"]["model"]
DATA_PATH = config["training"]["dataset_path"]


def check_images(directory):

    if not os.path.exists(directory):
        print(f"Error: Directory '{directory}' not found; exiting data check.")
        return False

    valid_extensions = {".jpg", ".jpeg", ".png"}
    files = os.listdir(directory)

    for file in files:
        if not any(file.lower().endswith(ext) for ext in valid_extensions):
            print(f"Error: {file} is not a valid image format; exiting data check.")
            return False

        try:
            img = Image.open(os.path.join(directory, file))
            img.verify()  # Verify image is readable
        except Exception as e:
            print(f"Corrupt image detected: {file} ({e}); exiting data check.")
            return False

    print(f"Finished checking images in {directory}")
    return True


def check_text_file(file_path):

    # Is file .json
    if not file_path.lower().endswith() == "json":
        print(f"Error: File '{file_path}' must be .json; exiting data check.")
        return False

    # Does file exist
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' not found; exiting data check.")
        return False

    # Is file empty
    if os.path.getsize(file_path) == 0:
        print(f"Error: File '{file_path}' is empty; exiting data check.")
        return False

    # Is data formatted correctly with keys/text and metadata/text (optional)
    with open("llm_keys.yaml", "r") as f:
        config = yaml.safe_load(f)

    TEXT_KEYS = set(config.get("text_keys", []))
    # METADATA_KEYS = set(config.get("metadata_keys", []))
    MIN_TEXT_WORDS = config.get("min_text_words", 5)

    with open(file_path, "r") as f:
        for line in f:
            try:
                data = json.loads(line.strip())

                # Ensure at least one valid text key exists (is this enough?)
                # Or maybe that we only have one key and as many metadata keys as we want????
                text = None
                for key in TEXT_KEYS:
                    if key in data and isinstance(data[key], str):
                        text = data[key].strip()
                        break  # Stop at the first

                if not text:
                    print(
                        f"Error: No valid text field found in entry: {data}; exiting data check."
                    )
                    return False

                # Enforce user-specified minimum word count
                if len(text.split()) < MIN_TEXT_WORDS:
                    print(
                        f"Error: Text too short in entry: {data}; exiting data check."
                    )
                    return False

            except json.JSONDecodeError:
                print(
                    f"Error: Invalid JSON format in line: {line}; exiting data check."
                )
                return False
    return True


def main():

    print(f"Checking dataset format for model: {MODEL_NAME}")

    if MODEL_NAME in ["resnet50", "resnet101", "mobilenet_v2", "inceptionv3", "unet"]:

        for folder in os.listdir(DATA_PATH):
            folder_path = os.path.join(DATA_PATH, folder)
            check = check_images(folder_path)
            return check

    elif MODEL_NAME == "unet":
        check = check_images(os.path.join(DATA_PATH, "images"))
        check = check_images(os.path.join(DATA_PATH, "masks"))

    elif MODEL_NAME in [
        "gpt2",
        "EleutherAI/gpt-j-6B",
        "mistralai/Mistral-7B",
        "meta-llama/Llama-2-7b-hf",
        "meta-llama/Llama-2-13b-hf",
    ]:
        with open("config_llm.yaml", "r") as f:
            config_llm = yaml.safe_load(f)

        data_filename = config_llm.get("data_filename")
        check = check_text_file(os.path.join(DATA_PATH, data_filename))
        return check

    elif MODEL_NAME == "dcgan":
        check = check_images(os.path.join(DATA_PATH, "real")) and check_images(
            os.path.join(DATA_PATH, "generated")
        )

    else:
        print(f"Model '{MODEL_NAME}' is not supported.")


if __name__ == "__main__":
    main()
