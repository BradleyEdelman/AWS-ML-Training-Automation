import os
import yaml
import pandas as pd
import tensorflow as tf
from PIL import Image

# Load config
with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

MODEL_NAME = config["training"]["model"]
DATA_PATH = config["training"]["dataset_path"]


def check_images(directory):

    if not os.path.exists(directory):
        print(f"Error: Directory '{directory}' not found!")
        return False

    valid_extensions = {".jpg", ".jpeg", ".png"}
    files = os.listdir(directory)
    
    for file in files:
        if not any(file.lower().endswith(ext) for ext in valid_extensions):
            print(f"Warning: {file} is not a valid image format!")
            return False
        
        try:
            img = Image.open(os.path.join(directory, file))
            img.verify()  # Verify image is readable
        except Exception as e:
            print(f"Corrupt image detected: {file} ({e})")
            return False
        
    print(f"Finished checking images in {directory}")
    return True

def check_text_file(file_path):
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' not found!")
        return False
    
    if os.path.getsize(file_path) == 0:
        print(f"Warning: File '{file_path}' is empty!")
        return False

    return True



def main():

    print(f"Checking dataset format for model: {MODEL_NAME}")

    if MODEL_NAME in ["resnet50", "inceptionv3"]:

        for folder in os.listdir(DATA_PATH):
            folder_path = os.path.join(DATA_PATH, folder) 
            check_images(folder_path)

    elif MODEL_NAME == "unet":
        check_images(os.path.join(DATA_PATH, "images"))
        check_images(os.path.join(DATA_PATH, "masks"))

    elif MODEL_NAME == "gpt2":
        check_text_file(os.path.join(DATA_PATH, "dataset.txt"))

    elif MODEL_NAME == "dcgan":
        check_images(os.path.join(DATA_PATH, "real")) and check_images(os.path.join(DATA_PATH, "generated"))

    # elif MODEL_NAME == "stable-diffusion":
        # check_text_file(os.path.join(DATASET_PATH, "prompts.txt"))
        # check_json_format(os.path.join(DATASET_PATH, "metadata.json"))
        # if os.path.exists(os.path.join(DATASET_PATH, "reference_images")):
        #     check_images(os.path.join(DATASET_PATH, "reference_images"))

    else:
        print(f"Model '{MODEL_NAME}' is not supported.")

if __name__ == "__main__":
    main()