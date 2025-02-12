# AWS ML Training Automation

This repository provides an automated workflow for setting up and running **LLM training on AWS EC2** with minimal manual effort. The goal is to allow users to easily launch, configure, and manage ML training instances while being mindful of modern trainin priorities like checkpointing and cost optimization.

## 🚀 Features
- **Automated EC2 deployment** for ML training
- **Pre-configured IAM setup guide** (since IAM roles must be manually requested)
- **SSH automation** for seamless instance access
- **Data fetching from S3** for training
- **Automatic checkpointing & resume training**
- **Instance monitoring & auto-shutdown** to avoid unnecessary costs
- **Customizable settings via `config.yaml`**

## 📂 File Structure (Estimated)
```
aws-ml-training-automation/
│── README.md  # Overview & setup instructions
│── iam_setup.md  # IAM role request guide
│── config.yaml  # User config for EC2, S3, model settings
│── setup/
│   ├── launch_ec2.sh  # Launches EC2 Spot Instance
│   ├── ssh_connect.sh  # Auto-SSH into EC2
│   ├── instance_status.sh  # Check EC2 status
│   ├── terminate_ec2.sh  # Stops EC2 after training
│── training/
│   ├── fetch_data.sh  # Downloads dataset from S3
│   ├── train_model.sh  # Starts model training
│   ├── save_checkpoint.sh  # Saves model checkpoint to S3
│   ├── resume_training.sh  # Resumes from latest checkpoint
│── scripts/
│   ├── deploy_training.sh  # Main automation script (calls everything)
│   ├── config.yaml.example  # Example user config file
```

## 🛠️ Setup Instructions
### 1. Request IAM Role Permissions
Since IAM roles require manual setup, refer to `iam_setup.md` for details on how to request access.

### 2. Configure AWS & Training Settings
Modify `config.yaml` with your AWS and ML training preferences.

### 3. Deploy Training
Run the following command to launch an EC2 instance and start training:
```bash
bash deploy_training.sh --model gpt2 --instance g4dn.xlarge
```

This script will:
✅ Launch an AWS GPU instance with the correct settings
✅ Connect via SSH
✅ Download the dataset from S3
✅ Resume training from the latest checkpoint (or start fresh)
✅ Save model progress every `X` epochs
✅ Shut down the EC2 instance when done

## 📌 Next Steps
- Implement `deploy_training.sh` (Main Automation Script)
- Finalize `config.yaml` for easy customization
- Add example Hugging Face GPT-2 fine-tuning script

