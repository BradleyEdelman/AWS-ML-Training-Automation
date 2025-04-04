# Config.yaml Guide

This document provides an explanation of the `config.yaml` file, which controls various parameters related to AWS setup, EC2 instance configuration, and ML training. Model-specific parameters are defined in separate files (`config_cnn.yaml`, `config_llm.yaml`) and are automatically applied when training a corresponding model.

---

## **Overview**
The `config.yaml` file is structured into three sections:

- `aws`: AWS-related settings (IAM role, S3 bucket, etc.)
- `ec2`: Spot Instance configuration (AMI, instance type, etc.)
- `training`: Model specification and training-specific parameters

---

## **AWS Configuration**
```yaml
aws:
  cli_profile: "ec2-training"          # AWS CLI profile used for authentication
  iam_role_arn: "arn:aws:iam::account-id:role/EC2-Training-Role"  # IAM role ARN
  iam_instance_profile: "EC2-Training-Role"  # Instance profile name for EC2 role assumption
  region: "region"                  # AWS region (e.g., us-east-1, eu-central-1)
  s3_bucket: "my-training-bucket"      # S3 bucket for datasets & checkpoints
  session_name: "EC2-Training-Session" # Name of the IAM session (for tracking)
```

IAM-related parameters should be automatically setup either manually or when using the [01_iam_role_setup.sh](bootsrap/01_iam_role_setup.sh) script. Parameters such as the **region** and **s3 bucket** will need to be customized based on the user's input.


## **EC2 Configuration**
```yaml
ec2:
  ami_id: "ami-0abcdef1234567890"    # Amazon Machine Image (AMI) ID
  instance_type: "g4dn.xlarge"       # EC2 instance type
  key_pair_name: "ec2-training-key"  # SSH key pair name
  volume_size: 50                    # Storage volume size in GB
  use_spot_instance: true            # Use Spot Instance (set to false for On-Demand instance)
```

Recommended AWS AMIs for ML:
"ami-0abcdef1234567890" AWS Deep Learning AMI (Ubuntu 20.04)
"ami-0123456789abcdef" NVIDIA GPU Optimized AMI
"ami-0987654321fedcba" AWS DL AMI with TensorFlow/PyTorch

Recommended Instance Types:
CPU Training: c5.xlarge, m5.large
Standard GPU: g4dn.xlarge (e.g. CNNs & small LLMs)
High-performance GPU: p3.2xlarge, p4d.24xlarge (e.g. LLMs & Stable Diffusion)
Multi-GPU Training: p5.48xlarge (e.g. LLaMA, GPT-3)


## **Training Configuration**
```yaml
training:
  model: "resnet50"                  # Model type (e.g., resnet50, gpt2, unet, etc.)
  dataset_path: "data/"              # Local dataset storage path on EC2 instance
  checkpoint_dir: "checkpoints/"     # Local checkpoint storage path on EC2 instance
  checkpoint_prefix: "checkpoint"    # Prefix for checkpoint filenames
  resume_from_checkpoint: true       # Resume training from latest checkpoint (false to train from scratch)
  epochs: 50                         # Number of training epochs
  fine_tune: true                    # Whether to fine-tune pre-trained models (false to retrain model)
```

Supported Models:
CNN Models: resnet50, inceptionv3
LLMs: gpt2, gpt-j-6b, mistral 7b
Generative Models: dcgan
Medical Image Processing: unet

Fine-tuning Behavior:
false: Train from scratch (not recommended)
true: Unfreeze layers & use pre-trained weights

---

## Guide for `config_cnn.yaml`
For CNN models, additional hyperparameters are defined here.

```yaml
model: "resnet50"           # Model type
num_layers_to_unfreeze: 20  # Number of layers to unfreeze during fine-tuning
learning_rate: 0.0001       # Optimizer learning rate
batch_size: 32              # Training batch size
optimizer: "adam"           # Optimizer type ("adam", "sgd", "rmsprop")
loss_function: "categorical_crossentropy"  # Loss function
metrics: ["accuracy"]       # Evaluation metrics
```

Supported CNN Architectures: 
standard: resnet50, resnet101, inceptionv3
Edge ML: mobilenet_v2
Segmentation: unet

Available Optimizers:
adam: Adaptive moment estimation, works well for CNNs
sgd: Standard stochastic gradient descent
rmsprop → Useful for deeper networks

Available Loss Functions:
categorical_crossentropy: Multi-class classification
binary_crossentropy: Binary classification
mse: Regression-based CNNs

---

## Guide for `config_llm.yaml`
For LLM models, the tokenizer, sequence length, batch size, and fine-tuning parameters are defined here:

```yaml
model: "gpt2"                  # Model type
tokenizer: "gpt2"              # Tokenizer for text processing
max_length: 512                # Maximum sequence length for tokenized input
batch_size: 8                  # Training batch size (depends on GPU memory)
learning_rate: 0.00005         # Optimizer learning rate
weight_decay: 0.01             # Weight decay for regularization
num_layers_to_unfreeze: 5      # Number of transformer layers to unfreeze during fine-tuning
gradient_accumulation_steps: 4 # Gradient accumulation (needed for large models)
use_fp16: true                 # Mixed-precision training for efficiency

```

### **Supported LLM Architectures**
| **Common Name** | **Hugging Face Model Name**                | **Parameters** | **Memory Requirement** | **Use Case** |
|---------------|--------------------------------|------------|--------------------|------------------------------|
| **GPT-2**     | `"gpt2"`                      | 125M       | ~2GB               | Small-scale text generation |
| **GPT-J 6B**  | `"EleutherAI/gpt-j-6B"`       | 6B         | ~24GB              | Medium-scale LLM for chatbots |
| **Mistral 7B**| `"mistralai/Mistral-7B"`      | 7B         | ~32GB              | High-efficiency language modeling |
| **LLaMA 2 7B** | `"meta-llama/Llama-2-7b-hf"` | 7B         | ~32GB              | Open-source large-scale LLM |
| **LLaMA 2 13B** | `"meta-llama/Llama-2-13b-hf"` | 13B      | ~64GB              | More powerful open-source LLM |


### **Tokenizer Mapping**
| **Common Name** | **Hugging Face Tokenizer Name** |
|---------------|--------------------------------|
| GPT-2         | `"gpt2"` |
| GPT-J 6B      | `"EleutherAI/gpt-j-6B"` |
| Mistral 7B    | `"mistralai/Mistral-7B"` |
| LLaMA 2 7B    | `"meta-llama/Llama-2-7b-hf"` |
| LLaMA 2 13B   | `"meta-llama/Llama-2-13b-hf"` |

### **Recommended Training Parameters**
| **Common Name** | **Batch Size** | **Gradient Accumulation**|
|---------------|------------------|--------------------------|
| GPT-2         | 4 | 1 |
| GPT-J 6B      | 2 | 1 |
| Mistral 7B    | 1 | 8 |
| LLaMA 2 7B    | 1 | 8 |
| LLaMA 2 13B   | 1 | 8 |

### **Recommended GPU Instances**
| **Common Name** | **Recommended AWS Instance** |
|---------------|------------------------------|
| GPT-2         | `g4dn.xlarge`, `g5.xlarge` |
| GPT-J 6B      | `p3.8xlarge`, `p4d.24xlarge` |
| Mistral 7B    | `p4d.24xlarge`, `p5.48xlarge` |
| LLaMA 2 7B    | `p5.48xlarge`, multi-GPU setups |
| LLaMA 2 13B   | `p5.48xlarge`, `p5.96xlarge` (multi-GPU) |