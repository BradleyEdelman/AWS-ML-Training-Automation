import yaml
import tensorflow as tf

# Load config
with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

MODEL_NAME = config["training"]["model"]
DATA_PATH = config["training"]["dataset_path"]


def prepare_cnn_data():
    
    print("Preparing Image Data for CNN...")

    with open("config_cnn.yaml", "r") as f:
        config_cnn = yaml.safe_load(f)

    BATCH_SIZE = config_cnn["batch_size"]

    # Load dataset and force to natural size of common CNN architectures
    dataset = tf.keras.utils.image_dataset_from_directory(
        directory=DATA_PATH,
        image_size=(224, 224),
        color_mode='rgb',
        batch_size=BATCH_SIZE,
        label_mode='categorical'
    )
    
    num_classes = len(dataset.class_names)
    print(f"Detected {num_classes} classes:")
    for i, class_name in enumerate(dataset.class_names):
        print(f"  Class {i}: {class_name}")

    print("CNN Data Preparation Complete.")
    return dataset

def prepare_llm_data():
    print("Preparing Text Data for GPT-2...")

    print("GPT-2 Data Preparation Complete.")



def main():
    print(f"Preparing data for model: {MODEL_NAME}")

    if MODEL_NAME in ["resnet50", "inceptionv3"]:
        return prepare_cnn_data()

    elif MODEL_NAME == "gpt2":
        return prepare_llm_data()
    
    else:
        print(f"Model '{MODEL_NAME}' is not supported.")


if __name__ == "__main__":
    main()