import yaml
import tensorflow as tf

# Load config
with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

MODEL_NAME = config["training"]["model"]
DATA_PATH = config["training"]["dataset_path"]


def prepare_cnn_data(DATA_PATH=DATA_PATH):
    print("Preparing Image Data for CNN...")
    import tensorflow as tf

    # Load dataset
    dataset = tf.keras.utils.image_dataset_from_directory(
        directory=DATA_PATH,
        image_size=(224, 224),
        batch_size=32
    )
    
    # Check dataset classes
    class_names = dataset.class_names
    print(f"Detected class labels: {class_names}")

    print("CNN Data Preparation Complete.")
    return dataset

def prepare_llm_data(DATA_PATH=DATA_PATH):
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