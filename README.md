# AWS ML Training Automation

This repository provides an automated workflow for setting up and running **deep learning training on AWS EC2** with minimal manual effort. The goal is to allow users to easily launch, configure, track, and manage EC2 instances during long ML training sessions while trying to minimize overall training cost.

I started this project since I wanted to get more involved in heavily ML models like LLMs and iamge generators, but cant run these models locally on my laptop/CPU architecture. On the other hand, AWS SageMaker is an additional cost and isnt very flexible, and GPUs in general are quite costly. Even fine-tuning some of these models with GPUs can take a few hours to days, so the costs can add up after a while. Therefore, I opted for using EC2 pot Instances, but also want to account for when AWS automatically shuts down the instance in the middle of training :(. I hope that model checkpointing can help users (and myself) not lose too much time by continuing training rather than starting over.

## **Features**
- **Spot Instance-Based ML Training** - Automatically launch annd manage AWS Spot Instances for cost-efficient model training.  
- **AWS IAM Role Setup Guide** - Pre-configured IAM policies with access to EC2, S3, and CloudWatch.  
- **SSH Automation** - Auto-generate SSH key for access to EC2 without manual setup.  
- **Spot Termination Detection and Checkpointing** - Detects when AWS plans to reclaim a Spot Instance and triggers checkpoint saving before shutdown.  
<!-- - **CloudWatch Logging** - Send logs to AWS CloudWatch for monitoring instance activity and debugging.    -->
- **Customizable Settings** - Use a simple **`config.yaml`** to modify instance type, dataset path, and training parameters.  
- **Auto-Shutdown** - Ensures EC2 instance is terminated after training completes to avoid extra costs.  

---

## 📂 File Structure (Estimated)
```
aws-ml-training-automation/
│── docs/
│   ├── 00_aws_cli_installation                 # Guide for installing AWS CLI and Git Bash
│   ├── 01_aws_iam_setup.md                     # AWS IAM role setup guide
│   ├── 02_aws_assume_role.md                   # Guide to assuming IAM role using AWS CLI
│   ├── 03_aws_S3_upload_data.md                # Guide for data upload using AWS CLI
│
│── example_files/
│   ├── iam_permissions_full.json               # Full IAM role permissions (e.g. root user)
│   ├── iam_permissions_restricted.json         # Restricted IAM role permissions
│   ├── iam_trust_policy.json                   # Trust policy
│
├── monitoring/
│   ├── cloudwatch_logs.sh (TBD)
|
│── scripts/
│   ├── deploy_training.sh (TBD)
|
│── setup/
│   ├── assume_iam_role.sh                      # Assumes IAM role
│   ├── iam_role_setup.sh (NOT TESTED)          # IAM role setup only using AWS CLI
│   ├── install_shell_requirements (NOT TESTED) # Installed shell requirments using Git Bash
│   ├── launch_spot_instance.sh                 # Requests a Spot Instance (and enable SSH)
│   ├── ssh_connect.sh                          # SSH into EC2 instance
│   ├── terminate_ec2.sh                        # Terminates EC2 instance
│   ├── detect_spot_termination.sh (TDB?)       # Detects AWS Spot termination
│
│── tests/
│
│── training/
│   ├── fetch_data.sh (TBD)                     # Download dataset from S3
│   ├── train_model.py (TBD)                    # Starts model training
│   ├── save_checkpoint.py (TBD)                # Saves model checkpoint to S3
│   ├── resume_training.sh (TBD)                # Resumes training from latest checkpoint
│
│── .gitignore
│── .pre-commit-config.yaml
│── CHANGELOAG.md
│── config.yaml
│── mypy.ini
│── pyproject.toml
│── README.md
│── requirements-sh.txt
│── requirements-dev.txt
│── requirements.txt
```

---

## 🛠️ Setup Instructions
### 1. Install and setup AWS CLI and Git Bash
Refer to [`00_aws_cli_installation.md`](docs/00_aws_cli_installation.md) for details on how to install AWS command line interface and Git Bash for running shell scripts.

### 2. Set up AWS IAM role
- Follow [`01_aws_iam_setup.md`](docs/01_aws_iam_setup.md) to request or create an IAM role with the necessary (or sufficient) permissions.

### 3. Configure AWS & Training Settings
Modify [`config.yaml`](config.yaml) with your AWS credentials, instance type, model settings, checkpoint preferences, etc.

### 4. Assume IAM role
- Assume your IAM role according to [`02_aws_assume_role.md`](docs/02_aws_assume_role.md) with proper permissions for accessing data, requesting spot intances and running scripts.

### 5. Upload Data to your S3 Bucket
- Upload datasets to S3 as described in [`03_aws_s3_upload_data.md`](docs/03_aws_s3_upload_data.md).

### 6. Training workflow
Use the following scripts, as needed, to launch an EC2 instance, start training, and handle interruptions:

## **Workflow Overview**

| **Step** | **Script** | **Purpose** |
|----------|-----------|-------------|
| **1. Assume IAM role** | [`iam_assume_role.sh`](setup/assume_iam_role.sh) | Assume IAM role with permissions |
| **1. Launch Spot Instance** | [`launch_spot_instance.sh`](setup/launch_spot_instance.sh) | Requests a new Spot Instance |
| **2. SSH into Instance** | [`ssh_connect.sh`](setup/ssh_connect.sh) | Automatically SSHs into the instance |
<!-- | **3. Fetch Data from S3** | [`fetch_data.sh`](training/fetch_data.sh) | Downloads dataset from S3 to the instance |
| **4. Start Training** | [`train_model.py`](training/train_model.py) | Runs the ML model training |
| **5. Monitor for Spot Termination** | [`detect_spot_termination.sh`](setup/detect_spot_termination.sh) | Detects AWS termination notice |
| **6. Save Checkpoint Before Shutdown** | [`save_checkpoint.py`](training/save_checkpoint.py) | Saves model checkpoint to S3 before shutdown |
| **7. Terminate EC2 Instance** | [`terminate_ec2.sh`](setup/terminate_ec2.sh) | Stops EC2 instance when training completes or Spot Instance is terminated |
| **8. Resume Training from Checkpoint** | [`resume_training.sh`](training/resume_training.sh) | Loads latest checkpoint & resumes training |
| **📊 Push Logs to CloudWatch** | [`cloudwatch_logs.sh`](monitoring/cloudwatch_logs.sh) | Tracks logs remotely | -->

## Contributions and Limitations
Contributions are welcomed:
- Reporting bugs or requesting features: [GitHub Issues](https://github.com/BradleyEdelman/AWS-ML-Training-Automation/issues)
- I'm getting more used to AWS CLI, but still not completely fluent and sometimes go back and forth with the Dashboard. This is also my first deep dive into heavy shell script use, and I'm by no means an expert. Hopefully my "automated" scripts work for others' setups - any feedback on if and where issues arise would be much appreciated!

## License
This project is licensed under the MIT License - see the LICENSE file for details.


<!-- 
---
# **Features directions**
- **Auto-Restart on Spot Interruption** - Automatically launch a new instance and restart training from the last checkpoint.  
- **Multi-Node Scaling** - Distribute training across multiple Spot Instances for faster model convergence.  
- **Automated Model Selection** - Adapt training strategy based on instance type (CPU/GPU, VRAM).  
- **Different ML Strategies** - Support for LLM, CNN, image generators, etc. -->



