# Config.yaml Guide

This document provides an explanation of the `config.yaml` file, which controls various parameters related to AWS setup, EC2 instance configuration, and ML training. Guides for model type-specific config files will come soon. 

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
  region: "region"                   # AWS region for resources (e.g. us-east-1)
  s3_bucket: "my-training-bucket"    # S3 bucket where datasets and checkpoints are stored
  iam_role_arn: "arn:aws:iam::account-id:role/EC2-Training-Role"  # IAM role ARN to be assumed
  cli_profile: "ec2-training"        # AWS CLI profile name
```

## **EC2 Configuration**
```yaml
ec2:
  ami_id: "ami-0abcdef1234567890"    # Amazon Machine Image (AMI) ID
  instance_type: "g4dn.xlarge"       # EC2 instance type
  key_pair_name: "ec2-training-key"  # SSH key pair name
  volume_size: 50                    # Storage volume size in GB
  use_spot_instance: true            # Use Spot Instance (set to false for On-Demand instance)
```

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