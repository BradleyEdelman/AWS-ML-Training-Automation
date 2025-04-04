import sys

import yaml  # type: ignore

# Load config files
with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

training_model = config["training"]["model"]
aws_config = config["aws"]
ec2_config = config["ec2"]
training_config = config["training"]

# Load CNN & LLM specific configs as needed
if training_model in ["resnet50", "resnet101", "inceptionv3"]:
    with open("config_cnn.yaml", "r") as f:
        config_cnn = yaml.safe_load(f)

elif training_model in [
    "gpt2",
    "EleutherAI/gpt-j-6B",
    "mistralai/Mistral-7B",
    "meta-llama/Llama-2-7b-hf",
    "meta-llama/Llama-2-13b-hf",
]:
    with open("config_llm.yaml", "r") as f:
        config_llm = yaml.safe_load(f)


def check_cnn_config():
    if not config_cnn:
        print("No CNN config loaded. Skipping CNN checks.")
        sys.exit(1)

    print("\nChecking CNN Configuration...")

    # Required keys
    required_keys = [
        "optimizer",
        "loss_function",
        "batch_size",
        "num_layers_to_unfreeze",
    ]
    for key in required_keys:
        if key not in config_cnn:
            print(f"Missing required key in config_cnn.yaml: '{key}'")
            sys.exit(1)

    # Batch size
    if config_cnn["batch_size"] > 64:
        print(
            f"Warning: Large batch size ({config_cnn['batch_size']}) may exceed GPU memory."
        )
        sys.exit(1)

    # Optimizer
    valid_optimizers = ["adam", "sgd", "rmsprop"]
    if config_cnn["optimizer"] not in valid_optimizers:
        print(
            f"Invalid optimizer: {config_cnn['optimizer']}. Must be one of {valid_optimizers}"
        )
        sys.exit(1)

    # Loss function
    valid_losses = ["categorical_crossentropy", "binary_crossentropy", "mse"]
    if config_cnn["loss_function"] not in valid_losses:
        print(
            f"Invalid loss function: {config_cnn['loss_function']}. Must be one of {valid_losses}"
        )
        sys.exit(1)

    # Layers to unfreeze (transfer learning)
    if config_cnn["num_layers_to_unfreeze"] < 1:
        print("Warning: num_layers_to_unfreeze < 1. Model may not be fine-tuned.")
        sys.exit(1)

    # Metrics
    if not isinstance(config_cnn.get("metrics", []), list):
        print("Error: 'metrics' should be a list (e.g., ['accuracy'])")
    elif not all(isinstance(m, str) for m in config_cnn["metrics"]):
        print("Error: each metric in 'metrics' should be a string.")

    print("CNN configuration checks passed.\n")


def check_llm_config():

    if not config_llm:
        sys.exit(1)

    print("\nChecking LLM Configuration...")

    # Ensure batch size is reasonable for large models
    if config_llm["batch_size"] > 4 and training_model in [
        "EleutherAI/gpt-j-6B",
        "mistralai/Mistral-7B",
        "meta-llama/Llama-2-7b-hf",
        "meta-llama/Llama-2-13b-hf",
    ]:
        print(
            f"Warning: Large batch size ({config_llm['batch_size']}) may exceed GPU memory for {training_model}."
        )

    # Ensure num_layers_to_unfreeze is valid
    if config_llm["num_layers_to_unfreeze"] < 0:
        print(
            f"Invalid number of layers to unfreeze: {config_llm['num_layers_to_unfreeze']}"
        )

    # Ensure tokenizer matches the model
    valid_tokenizer_mappings = {
        "gpt2": "gpt2",
        "EleutherAI/gpt-j-6B": "EleutherAI/gpt-j-6B",
        "mistralai/Mistral-7B": "mistralai/Mistral-7B",
        "meta-llama/Llama-2-7b-hf": "meta-llama/Llama-2-7b-hf",
        "meta-llama/Llama-2-13b-hf": "meta-llama/Llama-2-13b-hf",
    }

    if config_llm["tokenizer"] != valid_tokenizer_mappings.get(training_model, None):
        print(
            f"Tokenizer mismatch: Expected {valid_tokenizer_mappings[training_model]} but got {config_llm['tokenizer']}."
        )
        sys.exit(1)

    print("LLM configuration checks passed.\n")


def main():
    print("\nRunning Configuration Checks...")
    if training_model in ["resnet50", "resnet101", "inceptionv3"]:
        check_cnn_config()
    elif training_model in [
        "gpt2",
        "EleutherAI/gpt-j-6B",
        "mistralai/Mistral-7B",
        "meta-llama/Llama-2-7b-hf",
        "meta-llama/Llama-2-13b-hf",
    ]:
        check_llm_config()
    print("\nParameter validation completed.\n")


if __name__ == "__main__":
    main()
