# AWS ML Training Automation

This repository provides an automated workflow for setting up and running **deep learning training on AWS EC2** with minimal manual effort. The goal is to allow users to easily launch, configure, track, and manage EC2 instances during long ML training sessions while trying to minimize overall training cost.

I started this project since I wanted to get more involved in heavily ML models like LLMs and iamge generators, but cant run these models locally on my laptop/CPU architecture. On the other hand, AWS SageMaker is an additional cost and isnt very flexible, and GPUs in general are quite costly. Even fine-tuning some of these models with GPUs can take a few hours to days, so the costs can add up after a while. Therefore, I opted for using EC2 pot Instances, but also want to account for when AWS automatically shuts down the instance in the middle of training :(. I hope that model checkpointing can help users (and myself) not lose too much time by continuing training rather than starting over.

## **Features**
- **Spot Instance-Based ML Training** - Automatically launch annd manage AWS Spot Instances for cost-efficient model training.  
- **AWS IAM Role Setup Guide** - Pre-configured IAM policies with access to EC2, S3, and CloudWatch.  
- **SSH Automation** - Auto-generate SSH key for access to EC2 without manual setup.  
- **Spot Termination Detection and Checkpointing** - Detects when AWS plans to reclaim a Spot Instance and triggers checkpoint saving before shutdown.
- **Customizable Configuration** - Use **`config.yaml`** and model type-specific config files to modify instance type, dataset path, and training parameters
<!-- - **CloudWatch Logging** - Send logs to AWS CloudWatch for monitoring instance activity and debugging.    --> 
- **Auto-Shutdown** - Ensures EC2 instance is terminated after training completes to avoid extra costs.  

---

## 📂 File Structure (Estimated)
```
aws-ml-training-automation/
├── .github/
│   ├── workflows/
│   │   ├── ci.yml
│   │   ├── lint.yml
│
├── bootstrap/
│   ├── 00_install_shell_requirements_client.sh
│   ├── 01_iam_role_setup.sh
│
│── docs/
│   ├── 00_aws_cli_installation.md               # Guide for installing AWS CLI and Git Bash
│   ├── 01_aws_iam_setup.md                      # AWS IAM role setup guide
│   ├── 02_aws_assume_role.md                    # Guide to assuming IAM role using AWS CLI
│   ├── 03_aws_S3_upload_data.md                 # Guide for data upload using AWS CLI
│
│── example_files/
│   ├── iam_permissions_full.json                 # Full IAM role permissions (e.g. root user)
│   ├── iam_permissions_restricted.json           # Restricted IAM role permissions
│   ├── iam_trust_policy.json                     # Trust policy
|
├── ml/
│   ├── __init__.py
│   ├── checkpoint_load.py
│   ├── checkpoint_save.py
│   ├── data_check.py
│   ├── data_prepare.py
│   ├── model_configure.py
│   ├── train_model.py
│   ├── training_loops.py
│
├── requirements/
│   ├── requirements-dev.txt
│   ├── requirements-sh.txt
│   ├── requirements.txt
│
├── runtime_client/
│   ├── 02_assume_iam_role_client.sh
│   ├── 03_launch_spot_instance.sh
│   ├── 04_transfer_files.sh
│   ├── 05_ssh_connect.sh
│   ├── 06_terminate_ec2.sh
│   ├── script_client.sh
|
│── runtime_spot/
│   ├── monitoring/
│   │   ├── cloudwatch_logs.sh (TBD)
│   │   ├── detect_spot_termination.sh
│   ├── 06_install_requirements_spot.sh
│   ├── 07_assume_iam_role_spot.sh
│   ├── 08_fetch_data.sh
│   ├── script_spot_instance.sh
|
│── tests/
│
│── .gitignore
│── .pre-commit-config.yaml
│── CHANGELOG.md
│── config.yaml
│── config_cnn.yaml
│── config_llm.yaml
│── LICENSE
│── mypy.ini
│── pyproject.toml
│── README.md
```

---

## 🛠️ Setup Instructions
### 1. Install and setup AWS CLI and Git Bash
- Refer to [`00_aws_cli_installation.md`](docs/00_aws_cli_installation.md) to install **AWS CLI** and **Git Bash**.

### 2. Set up AWS IAM role
- Follow [`01_aws_iam_setup.md`](docs/01_aws_iam_setup.md) to request or create an **IAM role** with the necessary permissions.

### 3. Configure AWS & Training Settings
- Modify [`config.yaml`](config.yaml) to set up:
  - AWS IAM Role
  - Instance type
  - S3 bucket for dataset storage
  - Model training parameters
- Also modify model type-specific config files (e.g. `config_cnn.yaml`, `config_llm.yaml`)

### 4. Assume IAM role
- Assume your IAM role according to [`02_aws_assume_role.md`](docs/02_aws_assume_role.md) with proper permissions for accessing data, requesting spot intances and running scripts.

### 5. Upload Data to your S3 Bucket
- Upload datasets to S3 as described in [`03_aws_s3_upload_data.md`](docs/03_aws_s3_upload_data.md).

### 6. Workflow overview
The following scripts can be used to automatically access the AWS CLI, launch an EC2 instance, start training, and handle interruptions. This automation is split into **two major scripts**:  

1️. **`script_client.sh`** (Run from your local machine)  
2️. **`script_spot_instance.sh`** (Runs inside the AWS Spot Instance)  

Here is further information about what each of these scripts does. Further details about each step can be found in the linked script.
---

### **Client-Side Workflow: [`script_client.sh`](runtime_client/script_client.sh)**
| **Step**                | **Script** | **Description** |
|-------------------------|-----------|----------------|
| **1. Assume IAM Role** | [`02_assume_iam_role_client.sh`](runtime_client/02_assume_iam_role_client.sh) | Assumes AWS IAM role for authentication |
| **2. Launch Spot Instance** | [`03_launch_spot_instance.sh`](runtime_client/03_launch_spot_instance.sh) | Requests a new AWS Spot Instance |
| **3. Transfer Files** | [`04_transfer_files.sh`](runtime_client/04_transfer_files.sh) | Copies scripts, and configs to Spot Instance |
| **4. SSH into Instance** | [`05_ssh_connect.sh`](runtime_client/05_ssh_connect.sh) | Connects to Spot Instance |

---

### **Spot Instance Workflow [`script_spot_instance.sh`](runtime_spot/script_spot_instance.sh)**
| **Step**                | **Script** | **Description** |
|-------------------------|-----------|----------------|
| **5. Install Dependencies** | [`06_install_requirements_spot.sh`](runtime_spot/06_install_requirements_spot.sh) | Installs Python and shell dependencies |
| **6. Assume IAM Role (on Spot)** | [`07_assume_iam_role_spot.sh`](runtime_spot/07_assume_iam_role_spot.sh) | Ensures Spot Instance has proper AWS permissions |
| **7. Fetch Data from S3** | [`08_fetch_data.sh`](runtime_spot/08_fetch_data.sh) | Downloads dataset and previous training checkpoints from S3 |
| **8. Start Training** | [`train_model.py`](ml/train_model.py) | Runs ML training |
| **9. Detect Spot Termination** | [`detect_spot_termination.sh`](runtime_spot/monitoring/detect_spot_termination.sh) | Monitors for AWS Spot shutdown notice in the background |
| **10. Save Checkpoint** | [`checkpoint_save.py`](ml/checkpoint_save.py) | Saves training progress to S3 at specified intervals (epochs) |
| **11. Terminate EC2 Instance** | [`09_terminate_ec2.sh`](runtime_spot/09_terminate_ec2.sh) | Ensures cleanup and Spot Instance termination | 

---

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



