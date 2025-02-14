# AWS ML Training Automation

This repository provides an automated workflow for setting up and running **deep learning training on AWS EC2** with minimal manual effort. The goal is to allow users to easily launch, configure, and manage ML training instances while being mindful of modern trainin priorities like checkpointing and cost optimization.

## **Features**
- **Spot Instance-Based ML Training** - Automatically launch annd manage AWS Spot Instances for cost-efficient model training.  
- **AWS IAM Role Setup Guide** - Pre-configured IAM policies with restricted access to EC2, S3, and CloudWatch for enhanced security.  
- **SSH Automation** - Auto-retrieve public IP and SSH into EC2 without manual setup.  
- **Spot Termination Detection and Checkpointing** - Detects when AWS plans to reclaim a Spot Instance and triggers checkpoint saving before shutdown.  
- **CloudWatch Logging** - Send logs to AWS CloudWatch for monitoring instance activity and debugging.   
- **Customizable Settings** - Use a simple **`config.yaml`** to modify instance type, dataset path, and training parameters.  
- **Auto-Shutdown** - Ensures EC2 instance is terminated after training completes to avoid extra costs.  

---

## 📂 File Structure (Estimated)
```
aws-ml-training-automation/
│── docs/
│   ├── 01_aws_iam_setup.md          # AWS IAM role setup guide
│   ├── 02_aws_cli_setup.md          # AWS CLI setup & profile configuration
│   ├── 03_aws_S3_upload_data.md     # AWS data upload guide
│
│── example_files/
│   ├── EC2-Training-Role-permission-policy-example.json
│   ├── EC2-Training-Role-trust-policy-example.json
│
├── monitoring/                      # Logging & AWS notifications
│   ├── cloudwatch_logs.sh (TBD)     # Pushes logs to AWS CloudWatch
|
│── scripts/
│   ├── deploy_training.sh (TBD)     # Main automation script (calls everything)
|
│── setup/
│   ├── launch_spot_instance.sh      # Requests a Spot Instance dynamically
│   ├── ssh_connect.sh               # Auto-SSH into EC2 instance
│   ├── terminate_ec2.sh             # Stops EC2 after training
│   ├── detect_spot_termination.sh   # Detects AWS Spot termination
│
│── tests/
│
│── training/
│   ├── fetch_data.sh (TBD)          # Downloads dataset from S3
│   ├── train_model.py (TBD)         # Starts model training
│   ├── save_checkpoint.py (TBD)     # Saves model checkpoint to S3
│   ├── resume_training.sh (TBD)     # Resumes training from latest checkpoint
│
│── scripts/
│   ├── deploy_training.sh (TBD)     # Main automation script (calls everything)
│
│── .gitignore
│── .pre-commit-config.yaml
│── CHANGELOAG.md
│── config.yaml
│── mypy.ini
│── pyproject.toml
│── README.md                        # Overview & setup instructions
│── requirements-dev.txt
│── requirements.txt
```

---

## 🛠️ Setup Instructions
### 1. Obtain IAM Role Permissions
Since IAM roles require manual setup, refer to [`01_aws_iam_setup.md`](docs/01_aws_iam_setup.md) for details on how to obtain access.

### 2. Set up AWS CLI and upload data to S3 bucket
- Follow [`02_aws_cli_setup.md`](docs/02_aws_cli_setup.md) to configure the AWS CLI.
- Upload datasets to S3 as described in [`03_aws_s3_upload_data.md`](docs/03_aws_s3_upload_data.md).

### 3. Configure AWS & Training Settings
Modify [`config.yaml`](config.yaml) with your AWS credentials, instance type, model settings, and checkpoint preferences.

### 4. Training workflow
Use the following scripts, as needed, to launch an EC2 instance, start training, and handle interruptions:

## **Workflow Overview**

| **Step** | **Script** | **Purpose** |
|----------|-----------|-------------|
| **1. Launch Spot Instance** | [`launch_spot_instance.sh`](setup/launch_spot_instance.sh) | Requests a new Spot Instance dynamically |
| **2. SSH into Instance** | [`ssh_connect.sh`](setup/ssh_connect.sh) | Automatically SSHs into the instance |
| **3. Fetch Data from S3** | [`fetch_data.sh`](training/fetch_data.sh) | Downloads dataset from S3 to the instance |
| **4. Start Training** | [`train_model.py`](training/train_model.py) | Runs the ML model training |
| **5. Monitor for Spot Termination** | [`detect_spot_termination.sh`](setup/detect_spot_termination.sh) | Detects AWS termination notice |
| **6. Save Checkpoint Before Shutdown** | [`save_checkpoint.py`](training/save_checkpoint.py) | Saves model checkpoint to S3 before shutdown |
| **7. Terminate EC2 Instance** | [`terminate_ec2.sh`](setup/terminate_ec2.sh) | Stops EC2 instance when training completes or Spot Instance is terminated |
| **8. Resume Training from Checkpoint** | [`resume_training.sh`](training/resume_training.sh) | Loads latest checkpoint & resumes training |
| **📊 Push Logs to CloudWatch** | [`cloudwatch_logs.sh`](monitoring/cloudwatch_logs.sh) | Tracks logs remotely |

---

# **Features directions**
- **Auto-Restart on Spot Interruption** - Automatically launch a new instance and restart training from the last checkpoint.  
- **Multi-Node Scaling** - Distribute training across multiple Spot Instances for faster model convergence.  
- **Automated Model Selection** - Adapt training strategy based on instance type (CPU/GPU, VRAM).  
- **Different ML Strategies** - Support for LLM, CNN, image generators, etc.



